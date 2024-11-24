from flask import Flask, render_template, request, jsonify
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.prompts import ChatPromptTemplate
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
import openai
import os
import fitz  # PyMuPDF
import re
from typing import List, Tuple
import shutil
import urllib.parse

app = Flask(__name__)

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

FAISS_PATH = "faiss_db_opt"

# Keeping the same prompts
PLANNER_PROMPT = """You are a highly specialized separation processes expert with 25+ years of experience in industrial and academic settings. Analyze the given question and develop a rigorous technical approach that demonstrates advanced separation engineering expertise.

##Question Analysis##
First, categorize the question into one or more of these separation engineering domains:
- Distillation and Enhanced Distillation
- Liquid-Liquid Extraction
- Gas Absorption and Stripping
- Adsorption and Ion Exchange
- Membrane Separation Processes
- Crystallization
- Filtration and Centrifugation
- Drying Operations
- Evaporation
- Chromatographic Separations

Then, create a comprehensive plan to answer the following question. Your plan should cover all relevant aspects, including fundamental mass transfer concepts, equipment design, practical applications, and interrelationships between different separation principles.

Based solely on the following information from our database, create a plan to answer the question. Do not use any external knowledge.

##Available Tools##
1. SearchDoc: Search internal documents for relevant information.

##Output Format##
#Plan1: <describe your plan here>
#E1: <toolname>[<detailed query, specifying required information, equations, or concepts>]
#Plan2: <describe next plan>
#E2: <toolname>[<input here, you can use #E1 to represent its expected output>]
Continue until you have a comprehensive plan covering all aspects of the question.

##Your Task##
Create an extensive, detailed plan to answer the following question in the context of separation engineering: {question}

Ensure your plan covers:

1. Fundamental concepts
2. Relevant equations and their derivations
3. Interplay between different concepts when relevant.
4. Potential challenges or limitations when applicable.


##Now Begin##
"""

SOLVER_PROMPT = """As a separation processes specialist with extensive experience in industrial separation unit operations and academic research, generate a technically rigorous analysis that demonstrates deep expertise in the specific aspects of the problem presented.

##Plans and Evidences##
{plan_evidence}

##Your Task##
Generate a comprehensive technical analysis for: {question}

Remember to:
- Focus on the specific separation engineering challenge presented
- Fundamental concepts
- Provide relevant equations, balances, and formulas in Latex format (enclosed in $$ signs for inline equations and $$ for display equations)
- Address potential limitations and solutions when relevant
- Detail equipment design considerations in depth when applicable
- Include an illustrative example when possible

Throughout the report:
- Use LaTeX for all equations (enclosed in $$ signs for inline equations and $$ for display equations)
- Present mass and energy balances
- Include phase equilibrium relationships when applicable
- Detail mass transfer coefficients and driving forces
- Specify equipment dimensions and key design parameters

Ensure your report is technically accurate, detailed, and extensive. Do not hesitate to go into depth on relevant topics. Eliminate any references to books, authors, figures, or tables, numbered or named.

##Now Begin##
"""
class AIInterface:
    def __init__(self):
        self.embedding_function = OpenAIEmbeddings()
        # Initialize FAISS with safe loading
        if os.path.exists(FAISS_PATH):
            try:
                self.db = FAISS.load_local(
                    FAISS_PATH, 
                    self.embedding_function,
                    allow_dangerous_deserialization=True  # Only use if you trust the source of the index
                )
            except Exception as e:
                print(f"Error loading existing FAISS index: {e}")
                print("Creating new FAISS index...")
                # Create an empty FAISS index with sample data
                self.db = FAISS.from_texts(["placeholder"], self.embedding_function)
                self.db.save_local(FAISS_PATH)
        else:
            # Create an empty FAISS index with sample data
            if not os.path.exists(FAISS_PATH):
                os.makedirs(FAISS_PATH)
            self.db = FAISS.from_texts(["placeholder"], self.embedding_function)
            self.db.save_local(FAISS_PATH)
            
        self.planner_model = ChatOpenAI(
            temperature=0.7,
            model="gpt-3.5-turbo-16k",
            max_tokens=800,
        )
        self.solver_model = ChatOpenAI(
            temperature=0.2,
            model="gpt-3.5-turbo-16k",
            max_tokens=3500,
        )
        self.express_model = ChatOpenAI(
            temperature=0.3,
            model="gpt-3.5-turbo",
            max_tokens=1000,
        )
        self.file_db = None
        self.active_db = self.db
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )

    def save_db(self):
        """Safely save the current FAISS index"""
        try:
            if not os.path.exists(FAISS_PATH):
                os.makedirs(FAISS_PATH)
            self.db.save_local(FAISS_PATH)
        except Exception as e:
            print(f"Error saving FAISS index: {e}")

    def save_file_db(self):
        """Safely save the file-specific FAISS index"""
        try:
            if self.file_db is not None:
                if not os.path.exists('file_faiss'):
                    os.makedirs('file_faiss')
                self.file_db.save_local('file_faiss/current_file')
        except Exception as e:
            print(f"Error saving file FAISS index: {e}")

    def load_file_db(self):
        """Safely load the file-specific FAISS index"""
        try:
            if os.path.exists('file_faiss/current_file'):
                self.file_db = FAISS.load_local(
                    'file_faiss/current_file',
                    self.embedding_function,
                    allow_dangerous_deserialization=True
                )
                self.active_db = self.file_db
        except Exception as e:
            print(f"Error loading file FAISS index: {e}")
            self.file_db = None
            self.active_db = self.db


    def prepare_evidence(self, query_text: str) -> str:
        results = self.active_db.similarity_search_with_score(query_text, k=40)
        
        # Convert distances to similarity scores (0 to 1 scale)
        scores = [1 / (1 + score) for _, score in results]
        
        # Increase threshold for stricter filtering
        similarity_threshold = 0.7  # Increased from 0.5 for stricter matching
        
        filtered_results = [
            (doc, score) 
            for (doc, score) in zip((doc for doc, _ in results), scores)
            if score >= similarity_threshold
        ]

        if len(filtered_results) == 0:
            return "NO_RELEVANT_INFO"
        
        # Calculate average similarity score
        avg_similarity = sum(score for _, score in filtered_results) / len(filtered_results)
        
        # If average similarity is too low, return no info
        if avg_similarity < 0.65:  # Added additional threshold for average similarity
            return "NO_RELEVANT_INFO"
        
        sorted_results = sorted(filtered_results, key=lambda x: x[1], reverse=True)
        
        selected_chunks = []
        total_tokens = 0
        max_tokens = 1000
        
        for doc, score in sorted_results:
            chunk_tokens = len(doc.page_content.split())
            if total_tokens + chunk_tokens > max_tokens:
                break
            selected_chunks.append(doc.page_content)
            total_tokens += chunk_tokens
            print("selected_chunks",selected_chunks)

        return "\n\n---\n\n".join(selected_chunks)

    def generate_express_info(self, query_text: str) -> Tuple[str, str]:
        # Get evidence with improved filtering
        evidence = self.prepare_evidence_express(query_text)
        if evidence == "NO_RELEVANT_INFO":
            return "No relevant information found in the database. Please rephrase your query or check if this information exists in the uploaded documents.", "No Information Available"
        
        # Analyze query complexity
        is_direct_question = any([
            query_text.lower().startswith(starter) 
            for starter in ['what is', 'how does', 'explain', 'define', 'calculate', 'solve']
        ])
        
        # Adjust prompt based on query type
        if is_direct_question:
            express_prompt = f"""As an expert chemical engineer, provide a precise, technically accurate answer using ONLY the information below. 
            
            Question: {query_text}

            Available Information:
            {evidence}

            Requirements:
            1. Be direct and focused - answer exactly what was asked
            2. Include technical details and equations where relevant
            3. Use LaTeX for all equations (enclosed in $$ signs)
            4. Keep the response between 100-200 words
            5. If any specific detail isn't in the provided information, state that explicitly
            6. Start with the direct answer, then provide brief supporting details

            Remember: Only use information from the provided content."""

        else:
            express_prompt = f"""As an expert chemical engineer, synthesize a comprehensive answer using ONLY the information below.
            
            Question: {query_text}

            Available Information:
            {evidence}

            Requirements:
            1. Provide a structured response covering key aspects
            2. Include technical details and equations where relevant
            3. Use LaTeX for all equations (enclosed in $$ signs)
            4. Keep the response between 200-400 words
            5. If any specific detail isn't in the provided information, state that explicitly
            6. Break down complex concepts into clear explanations

            Format:
            - Start with a brief overview
            - Present key technical points
            - Include practical implications if relevant
            
            Remember: Only use information from the provided content."""

        # Use a lower temperature for direct questions
        if is_direct_question:
            self.express_model.temperature = 0.1
        else:
            self.express_model.temperature = 0.3

        response = self.express_model.predict(express_prompt)
        
        # Post-process the response
        processed_response = self.process_latex_equations(response)
        
        # Extract title and content
        lines = processed_response.split('\n')
        title = lines[0].strip() if lines else "Chemical Engineering Analysis"
        content = '\n'.join(lines[1:]).strip() if len(lines) > 1 else processed_response
        
        # Additional quality checks
        if len(content.split()) < 50:
            return "The available information is insufficient to provide a meaningful answer.", "No Information Available"
        
        if "not available" in content.lower() and len(content.split()) < 100:
            return "The requested information is not sufficiently covered in the database.", "No Information Available"
                
        return content, title

    def prepare_evidence_express(self, query_text: str) -> str:
        # Get more context for better answers
        results = self.active_db.similarity_search_with_score(query_text, k=25)
        
        # Improved similarity score calculation
        scores = [1 / (1 + score) for _, score in results]
        
        # Dynamic threshold based on query complexity
        words_in_query = len(query_text.split())
        base_threshold = 0.65
        threshold_adjustment = min(0.1, words_in_query * 0.01)
        similarity_threshold = base_threshold - threshold_adjustment
        
        filtered_results = [
            (doc, score) 
            for (doc, score) in zip((doc for doc, _ in results), scores)
            if score >= similarity_threshold
        ]

        if len(filtered_results) == 0:
            return "NO_RELEVANT_INFO"
        
        # Calculate weighted average similarity
        weights = [1.2 ** -i for i in range(len(filtered_results))]  # Exponential decay
        weighted_scores = [score * weight for (_, score), weight in zip(filtered_results, weights)]
        avg_similarity = sum(weighted_scores) / sum(weights)
        
        if avg_similarity < 0.6:
            return "NO_RELEVANT_INFO"
        
        sorted_results = sorted(filtered_results, key=lambda x: x[1], reverse=True)
        
        selected_chunks = []
        total_tokens = 0
        max_tokens = 1200  # Increased for better context
        
        current_context = set()
        
        for doc, score in sorted_results:
            chunk_tokens = len(doc.page_content.split())
            chunk_content = doc.page_content.lower()
            
            # Check for content overlap to avoid redundancy
            chunk_words = set(chunk_content.split())
            overlap_ratio = len(chunk_words.intersection(current_context)) / len(chunk_words) if chunk_words else 1
            
            if overlap_ratio < 0.7:  # Allow some overlap but not too much
                if total_tokens + chunk_tokens > max_tokens:
                    break
                selected_chunks.append(doc.page_content)
                total_tokens += chunk_tokens
                current_context.update(chunk_words)
        
        return "\n\n---\n\n".join(selected_chunks)

    def process_file(self, file_path: str):
        if file_path.endswith('.pdf'):
            text = self.extract_text_from_pdf(file_path)
        elif file_path.endswith('.txt'):
            with open(file_path, 'r') as file:
                text = file.read()
        else:
            raise ValueError("Unsupported file type")

        chunks = self.text_splitter.split_text(text)
        
        # Create a new FAISS index for the file
        self.file_db = FAISS.from_texts(chunks, self.embedding_function)
        self.active_db = self.file_db
        
        # Optionally save the file_db
        if not os.path.exists('file_faiss'):
            os.makedirs('file_faiss')
        self.file_db.save_local('file_faiss/current_file')

    def clear_file_data(self):
        self.file_db = None
        self.active_db = self.db
        # Clean up file FAISS index if it exists
        if os.path.exists('file_faiss'):
            shutil.rmtree('file_faiss')

    # Keeping the same methods without changes
    def generate_plan(self, query_text: str) -> str:
        evidence = self.prepare_evidence(query_text)
        if evidence == "NO_RELEVANT_INFO":
            return "NO_RELEVANT_INFO"
        
        planner_prompt = ChatPromptTemplate.from_template(PLANNER_PROMPT)
        prompt = planner_prompt.format(question=query_text)
        print(self.planner_model.predict(prompt))
        return self.planner_model.predict(prompt)

    def execute_plan(self, plan: str, query_text: str) -> str:
        if plan == "NO_RELEVANT_INFO":
            return "NO_RELEVANT_INFO"
        
        steps = plan.split('\n')
        evidences = []
        for step in steps:
            if step.startswith('#E'):
                if '[' in step:
                    tool, query = step.split('[', 1)
                    query = query.rstrip(']')
                else:
                    continue
                
                if 'SearchDoc' in tool:
                    evidence = self.prepare_evidence(query)
                    if evidence == "NO_RELEVANT_INFO":
                        return "NO_RELEVANT_INFO"
                    evidences.append(f"{step}\n{evidence}")
                    continue
        
        if not evidences:
            return "NO_RELEVANT_INFO"
        
        plan_evidence = '\n\n'.join(evidences)
        solver_prompt = ChatPromptTemplate.from_template(SOLVER_PROMPT)
        prompt = solver_prompt.format(plan_evidence=plan_evidence, question=query_text)
        return self.solver_model.predict(prompt)

    def generate_detailed_report(self, query_text: str) -> Tuple[str, str]:
        plan = self.generate_plan(query_text)
        if plan == "NO_RELEVANT_INFO":
            return "Unable to find relevant information in the database.", "No Information Available"
        
        response = self.execute_plan(plan, query_text)
        if response == "NO_RELEVANT_INFO":
            return "Unable to find relevant information in the database.", "No Information Available"
        
        processed_response = self.process_latex_equations(response)
        
        # Check for None response and handle it
        if processed_response is None:
            return "NO RELEVANT INFO", "Report Title"  # Return an appropriate title if needed
        
        # Now assign processed_response to content
        content = processed_response  # Define 'content' here
        print(f"Processed Response: {content}")  # Debugging line

        # Count words in content
        word_count = len(content.split())  # Using 'content' now
        print(f"Word Count: {word_count}")  # Debugging word count

        lines = content.split('\n')  # Split content into lines
        print("Lines:", lines)  # Debugging lines
        # Process lines as needed
        return "\n".join(lines), "Report Title"  # Return the processed lines and title


    def process_latex_equations(self, text: str) -> str:
        def replace_equation(match):
            latex_eq = match.group(1).strip()
            # Encode LaTeX string for URL
            encoded_latex = urllib.parse.quote(latex_eq)
            is_inline = not ('\n' in latex_eq or '\\begin{' in latex_eq or '\\end{' in latex_eq)
            
            if is_inline:
                # Inline equations
                return f'<span class="inline-equation"><img src="https://latex.codecogs.com/svg.latex?{encoded_latex}" alt="{latex_eq}" style="vertical-align: middle;"></span>'
            else:
                # Display equations
                return f'<div class="display-equation"><img src="https://latex.codecogs.com/svg.latex?{encoded_latex}" alt="{latex_eq}"></div>'

        # Process all LaTeX equations (both inline and display)
        text = re.sub(r'\$\$(.*?)\$\$', replace_equation, text, flags=re.DOTALL)
        text = re.sub(r'\$(.*?)\$', replace_equation, text)

        # Wrap non-equation text in paragraph tags
        paragraphs = text.split('\n')
        processed_paragraphs = []
        for paragraph in paragraphs:
            if not paragraph.strip().startswith('<div class="display-equation">'):
                paragraph = f'<p>{paragraph}</p>'
            processed_paragraphs.append(paragraph)

        return '\n'.join(processed_paragraphs)
        

    @staticmethod
    def extract_text_from_pdf(file_path: str) -> str:
        pdf_document = fitz.open(file_path)
        text = ""
        for page in pdf_document:
            text += page.get_text()
        return text

# Initialize the AI interface
ai_interface = AIInterface()

from flask import Flask, request, jsonify, send_file
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
import os

@app.route('/generate-pdf', methods=['POST'])
def generate_pdf():
    data = request.json
    content = data.get('content', '')

    pdf_path = r"C:\Users\AyoubFrikhat\Downloads\Solvi.v2\Solvi Latex Jabran\res.pdf"

    try:
        # Create PDF document
        doc = SimpleDocTemplate(pdf_path, pagesize=letter)
        styles = getSampleStyleSheet()

        justified_style = ParagraphStyle(
            name='Justified',
            parent=styles['BodyText'],
            alignment=4  # Justify
        )

        subtitle_style = ParagraphStyle(
            name='Subtitle',
            parent=styles['Heading2'],
            fontSize=12,
            spaceAfter=6,
            textColor='#052179',
            fontName='Helvetica-Bold'
        )

        story = []
        story.append(Paragraph("Solvi Report", styles['Title']))
        story.append(Spacer(1, 12))

        # Splitting the content into paragraphs
        paragraphs = content.split('\n\n')
        for i, part in enumerate(paragraphs):
            part = part.strip()
            if part.startswith("**") and part.endswith("**"):
                # Removing stars and making the subtitle bold
                subtitle = part.strip('**').strip()
                story.append(Paragraph(subtitle, subtitle_style))
                story.append(Spacer(1, 6))
            else:
                if i > 0:
                    story.append(Spacer(1, 6))  # Add space between paragraphs
                story.append(Paragraph(part, justified_style))
                story.append(Spacer(1, 12))

        doc.build(story)

        # Serve the PDF file
        return send_file(pdf_path, as_attachment=True)

    except Exception as e:
        # If there is any error, return a 500 error with the message
        return jsonify({'error': str(e)}), 500

@app.route('/')
def index():
    return render_template('indexios4.html')

@app.route('/query', methods=['POST'])
def query():
    data = request.json
    query_text = data['query']
    is_detailed = data['isDetailed']
    
    if is_detailed:
        response, title = ai_interface.generate_detailed_report(query_text)
    else:
        response, title = ai_interface.generate_express_info(query_text)
    
    if title == "No Information Available":
        return jsonify({
            'error': True,
            'message': 'No relevant information found in the database.',
            'title': 'No Information Available'
        }), 200  # Return 200 OK, but with an error flag
    
    return jsonify({
        'error': False,
        'response': response,
        'title': title
    })

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    if file:
        filename = file.filename
        file_path = os.path.join('uploads', filename)
        file.save(file_path)
        try:
            ai_interface.process_file(file_path)
            return jsonify({'message': f'File {filename} processed successfully'})
        except Exception as e:
            return jsonify({'error': str(e)})

@app.route('/clear', methods=['POST'])
def clear_file_data():
    ai_interface.clear_file_data()
    return jsonify({'message': 'File data cleared'})

if __name__ == '__main__':
    app.run(debug=True)
