import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import pytz

SCOPES = ['https://www.googleapis.com/auth/calendar']
TOKEN_FILE = "token.json"
CREDENTIALS_FILE = "credentials.json"
TIMEZONE = "Africa/Addis_Ababa"
tz = pytz.timezone(TIMEZONE)

def get_calendar_service():
    """Authenticate and return a Google Calendar API service instance."""
    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=8080)
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())
    service = build('calendar', 'v3', credentials=creds)
    return service

def create_event(title, start_dt, end_dt, attendees_emails=None, description=""):
    """Create a Google Calendar event with optional attendees and description."""
    service = get_calendar_service()
    event_body = {
        "summary": title,
        "description": description,
        "start": {"dateTime": start_dt.isoformat(), "timeZone": TIMEZONE},
        "end": {"dateTime": end_dt.isoformat(), "timeZone": TIMEZONE},
    }
    if attendees_emails:
        event_body["attendees"] = [{"email": email} for email in attendees_emails]

    created_event = service.events().insert(
        calendarId="primary",
        body=event_body,
        sendUpdates="all"
    ).execute()

    return created_event
