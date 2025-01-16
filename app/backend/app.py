from flask import Flask, render_template, request, jsonify, send_file, Response, g
from dotenv import load_dotenv
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
import os
import openai
from prometheus_client import start_http_server, Summary, Counter, Gauge, Histogram, generate_latest, CONTENT_TYPE_LATEST
import time

#Importing utils
from utils.U1_FilesUtils import U1_FilesUtils

#Importing services
from services.S1_PromptLogic import S1_PromptLogic
from services.S2_ClassifierLogic import Classifier
from services.S2_ClassifierLogic import PlannerAgent
from services.S4_SolverAgents import SuperSolverAgent
from services.mongo_db_utils import start_new_conversation, handle_user_message

from flask_mysqldb import MySQL
from flask import Flask, render_template, request, flash, redirect, url_for
from flask_bcrypt import Bcrypt
from MySQLdb.cursors import DictCursor  # Ensure this import is added
from flask import session

from itsdangerous import URLSafeTimedSerializer
from services.users_utils import insert_user, get_user_by_username, update_user_password
from services.email_utils import send_email
from services.llm_utils import instantiate_llm_model, get_json_from_response
from services.config_utils import load_config, get_config
from flask_cors import CORS
import json


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
CORS(app)  # Enable CORS for all routes


bcrypt = Bcrypt(app)


app.config['MYSQL_USER'] = os.getenv("MYSQL_USER")  
app.config['MYSQL_PASSWORD'] = os.getenv("MYSQL_PASSWORD") 
app.config['MYSQL_DB'] = os.getenv("MYSQL_DB") 
app.config['MYSQL_HOST'] = os.getenv("MYSQL_HOST")  # Docker service name


app.secret_key = os.getenv("secret_key")  # Use a long, random string


# Token serializer for secure password recovery links
serializer = URLSafeTimedSerializer(app.secret_key)


# Create MySQL instance
mysql = MySQL(app)



# Example metrics
REQUEST_COUNT = Counter('flask_requests_total', 'Total number of requests', ['method', 'endpoint'])
REQUEST_SIZE = Histogram('flask_request_size_bytes', 'Request size in bytes', ['method', 'endpoint'])
RESPONSE_SIZE = Histogram('flask_response_size_bytes', 'Response size in bytes', ['method', 'endpoint'])
STATUS_CODES = Counter('flask_status_code_total', 'Total responses by status code', ['status_code'])
REQUEST_DURATION = Summary('flask_request_duration_seconds', 'Duration of each request in seconds', ['method', 'endpoint'])



# Define the endpoint(s) you want to monitor
MONITORED_ENDPOINTS = ['generate-pdf', 'query', 'upload', 'clear']

@app.before_request
def before_request():
    if request.endpoint in MONITORED_ENDPOINTS:
        # Record the start time for latency
        g.start = time.time()
        g.request_size = request.content_length or 0


@app.after_request
def after_request(response):
    if request.endpoint in MONITORED_ENDPOINTS:
        # Increment the request counter
        REQUEST_COUNT.labels(method=request.method, endpoint=request.endpoint).inc()

        REQUEST_SIZE.labels(method=request.method, endpoint=request.endpoint).observe(g.request_size)


        processing_time = time.time() - g.start

        REQUEST_DURATION.labels(method=request.method, endpoint=request.endpoint).observe(processing_time)


        STATUS_CODES.labels(status_code=response.status_code).inc()

    return response


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
    user_input = data['query']
    is_detailed = data['isDetailed']

    # Initialize the classifier and classify the query
    classifier_model = Classifier()
    response = classifier_model.classify_query(user_input)
    print("\nRaw Classifier Response:\n")
    print(response)
    

    #response = json.dumps(response)
    classification_result = get_json_from_response(response)
    print("type(classification_result) : ",type(classification_result))
    # Parse the JSON response from the classifier, handle potential errors if JSON is not returned
    try:
        # classification_result = json.loads(response)
        print("\nClassification Result:\n")
        print(json.dumps(classification_result, indent=4))
    except json.JSONDecodeError:
        print("Error: The classifier returned an invalid JSON string. Please check the prompt or LLM output")
        return


    # Initialize planner agents based on the classification result
    planner_agents = []

    # Error handling for agent_allocation
    if (
            "agent_allocation" in classification_result and
            "selected_agents" in classification_result["agent_allocation"] and
            isinstance(classification_result["agent_allocation"]["selected_agents"], list)
       ):
         for agent_data in classification_result["agent_allocation"]["selected_agents"]:
            planner_agents.append(PlannerAgent(agent_data["agent_name"],agent_data["role"]))
    else:
        print("Error: The 'agent_allocation' structure or 'selected_agents' is missing or has incorrect type in the classification result. Check LLM output or your classifier prompt")
        return

    # Generate plans for each selected agent
    agent_plans = {}
    for planner in planner_agents:
        agent_plans[planner.agent_name] = planner.create_plan(
            classification_result["query_analysis"],
            classification_result["agent_allocation"]
        )
    print("\nIndividual Agent Plans:\n")
    for agent, plan in agent_plans.items():
         print(f"Agent: {agent}\nPlan:\n {plan}\n")


    # Execute the plans and retrieve evidence
    retrieved_evidence = {}
    for planner in planner_agents:
        retrieved_evidence[planner.agent_name] = planner.execute_plan(agent_plans[planner.agent_name])
    
    print("\nRetrieved Evidence:\n")
    for agent, evidence in retrieved_evidence.items():
          print(f"Agent: {agent}\nEvidence:\n {json.dumps(evidence, indent=4)}\n")
    
    # Initialize and execute the Super Solver agent
    super_solver = SuperSolverAgent("Super Solver", "Comprehensive Engineering Analysis")
    
    # Collect all the plans and retrieved evidence
    all_plans = agent_plans
    all_evidence = retrieved_evidence

    # Execute the super solver agent to generate the final report
    final_report = super_solver.execute_plan(
        "", # No plan is needed for the SuperSolver
        all_evidence, # Pass all the retrieved evidence
        user_input,  # Pass the original user input query
        classification_result["agent_allocation"], # Pass the classification for the solver to extract the other agents
    )

    print("\nFinal Report:\n")
    print(final_report)
    title = "test"
    
    
    user_id = "user123"  # Unique identifier for the user
    conversation_id = start_new_conversation(user_id)  # Start a new conversation
    print("conversation_id : ",conversation_id)
    
    assistant_answer = final_report['report']
    
    # Update the conversation history
    handle_user_message(user_id, conversation_id, user_input, assistant_answer)
    
    
    if title == "No Information Available":
        return jsonify([{
            'error': True,
            'content': 'No relevant information found in the database.',
            'title': 'No Information Available'
        }]), 200  # Return 200 OK, but with an error flag
        
    
    return jsonify([{
        'error': False,
        'content': assistant_answer,
        'title': title,
        'type': 'technical'
    }])

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


# Route for login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Check user credentials using the utility function
        user = get_user_by_username(mysql, username)
        
        if user and bcrypt.check_password_hash(user['password'], password):
            session['loggedin'] = True
            session['username'] = user['username']
            flash('Login successful!', 'success')
            return redirect('/')
        else:
            flash('Invalid username or password', 'danger')
    
    return render_template('login.html')


# Route for sign-up page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        
        try:
            # Insert user using the utility function
            insert_user(mysql, username, hashed_password)
            flash('Account created successfully! You can now log in.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            flash(f'Error: {str(e)}', 'danger')
    
    return render_template('signup.html')


@app.route('/logout', methods=['POST'])
def logout():
    session.pop('loggedin', None)
    session.pop('username', None)
    
    flash('You have been logged out.', 'success')
    
    return redirect(url_for('login'))


# Route for password recovery
@app.route('/recover', methods=['GET', 'POST'])
def recover():
    if request.method == 'POST':
        email = request.form['email']
        print("email : ",email)
        # Get user by email
        user = get_user_by_username(mysql, email)
        print("len(user) : ",len(user))
        print("user : ",user)
        if user:
            user_id = user['id']
            username = user['username']

            token = serializer.dumps(email, salt='password-recovery-salt')
            reset_link = f"{request.host_url}reset_password/{token}"

            subject = "Password Reset Request"
            message = f"""Hi {username},
            
Click the link below to reset your password:
{reset_link}

This link will expire in 30 minutes. If you did not request this, please ignore this email.
"""



            if send_email(subject, message, email):
                flash('A password reset link has been sent to your email.', 'success')
            else:
                flash('There was an error sending the email. Please try again later.', 'danger')
        else:
            flash('This email is not registered in our system.', 'danger')

        return redirect(url_for('recover'))
    return render_template('recover.html')


# Route for resetting the password
@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    try:
        email = serializer.loads(token, salt='password-recovery-salt', max_age=3600)
    except Exception:
        flash('The password reset link is invalid or has expired.', 'danger')
        return redirect(url_for('recover'))
    
    if request.method == 'POST':
        new_password = request.form['password']
        hashed_password = bcrypt.generate_password_hash(new_password).decode('utf-8')
        
        # Update password using the utility function
        update_user_password(mysql, email, hashed_password)
        
        flash('Your password has been updated successfully!', 'success')
        return redirect(url_for('login'))
    
    return render_template('reset_password.html')


# Expose metrics to Prometheus
@app.route("/metrics")
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

if __name__ == '__main__':
    app.run(debug=True)
