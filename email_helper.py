import requests
import os
from dotenv import load_dotenv

load_dotenv()
BREVO_API_KEY = os.getenv('BREVO_API_KEY')
BREVO_URL = 'https://api.brevo.com/v3/smtp/email'

def send_email(to_email, subject, content):
    data = {
        "sender": {"name": "Executive Assistant", "email": "edennigusie346@gmail.com"},
        "to": [{"email": to_email}],
        "subject": subject,
        "htmlContent": content
    }
    headers = {
        'accept': 'application/json',
        'api-key': BREVO_API_KEY,
        'content-type': 'application/json'
    }
    try:
        response = requests.post(BREVO_URL, json=data, headers=headers)
        return response.status_code == 201
    except Exception as e:
        print(f"Email sending error: {e}")
        return False