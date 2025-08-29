import google.generativeai as genai
import os
import json
import re
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

def parse_command(command):
    """
    Parse user command using Gemini AI and return structured JSON.
    """
    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt = f"""
    Parse this command for an executive assistant: "{command}".
    Return a JSON object with two keys:
    - 'intent': 'schedule', 'email', or 'remind'
    - 'details': relevant entities like person, email, date, time, subject, content
    Example:
    "Schedule a meeting with John next Tuesday at 10 AM" -> 
    {{
        "intent": "schedule",
        "details": {{
            "person": "John",
            "email": "edennigusie346@gmail.com",
            "date": "next Tuesday",
            "time": "10 AM"
        }}
    }}
    """
    try:
        response = model.generate_content(prompt)
        text_output = response.text.strip()
        # Remove code fences if present
        text_output = re.sub(r"^```(?:json)?\s*|\s*```$", "", text_output.strip(), flags=re.MULTILINE)
        parsed_json = json.loads(text_output)
        return parsed_json
    except json.JSONDecodeError:
        print("Failed to parse model output as JSON. Raw output:")
        print(text_output)
        return None
    except Exception as e:
        print(f"Error during command parsing: {e}")
        return None
