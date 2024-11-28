from flask import Flask, render_template, request, jsonify, send_file
from dotenv import load_dotenv
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
import os
import openai

#Importing utils
from utils.U1_FilesUtils import U1_FilesUtils

#Importing services
from services.S1_PromptLogic import S1_PromptLogic

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Set the path to the FAISS index
FAISS_PATH = "faiss_db_opt"

# Load prompts 
PLANNER_PROMPT = U1_FilesUtils.load_prompt("prompts/planner_prompt.txt")
SOLVER_PROMPT = U1_FilesUtils.load_prompt("prompts/solver_prompt.txt")

# Create an instance of the PromptLogic class
prompt_logic = S1_PromptLogic(planner_prompt=PLANNER_PROMPT, solver_prompt=SOLVER_PROMPT, faiss_path=FAISS_PATH)

app = Flask(__name__)

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
    return render_template('index.html')

@app.route('/query', methods=['POST'])
def query():
    data = request.json
    query_text = data['query']
    is_detailed = data['isDetailed']
    
    if is_detailed:
        response, title = prompt_logic.generate_detailed_report(query_text)
    else:
        response, title = prompt_logic.generate_express_info(query_text)
    
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
            prompt_logic.process_file(file_path)
            return jsonify({'message': f'File {filename} processed successfully'})
        except Exception as e:
            return jsonify({'error': str(e)})

@app.route('/clear', methods=['POST'])
def clear_file_data():
    prompt_logic.clear_file_data()
    return jsonify({'message': 'File data cleared'})

if __name__ == '__main__':
    app.run(debug=True)
