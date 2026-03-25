# Executive Assistant AI

**Executive Assistant AI** is a Python-based personal assistant that understands natural language commands to **schedule meetings**, **send email notifications**, and **provide daily reminders** using **Google Calendar API**, **Brevo Email API**, and **AI-powered command parsing**.

## 🚀 Features
- 🗣 **Natural Language Commands** – e.g., `Schedule a meeting with John next Tuesday at 10:30 AM for 45 minutes`.
- 📅 **Google Calendar Integration** – Automatically creates events with attendees.
- 📧 **Email Notifications** – Sends invites and confirmations.
- ⏰ **Daily Reminders** – Automatic daily task/meeting reminders.
- 🔄 **Error Handling** – Detects invalid emails and unknown commands.
## 🐳 Run with Docker

```bash
docker build -t executive-ai .
docker run executive-ai

## Tech Stack
- Python 3.x
- Google Calendar API
- Brevo Email API
- Google Gemini API

## 📂 Project Structure
executive-assistant-ai/
│── main.py # Main application loop
│── gemini_helper.py # AI command parsing logic
│── calendar_helper.py # Google Calendar event creation
│── email_helper.py # Email sending via Brevo
│── reminder.py # Daily reminders scheduler
│── requirements.txt # Dependencies
│── .gitignore # Ignore virtual env, cache files

Install dependencies:
pip install -r requirements.txt
Run:
python main.py
