import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os 

load_dotenv()

# Function to send email
def send_email(subject, message, to_email):
    try:
        
        from_email = os.getenv("communication_email")
        password = os.getenv("communication_email_password")
            
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587  # For SSL: 465, for TLS: 587

        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(message, 'plain'))

        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(from_email, password)
        server.sendmail(from_email, to_email, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return False