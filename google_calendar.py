import os

from django import setup
from django.conf import settings
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# Set up Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
setup()

# Scopes required for accessing Google Calendar API
SCOPES = ['https://www.googleapis.com/auth/calendar']


def get_credentials():
    creds = None
    token_path = os.path.join(settings.BASE_DIR, 'token.json')
    credentials_file = os.path.join(settings.BASE_DIR, 'credentials.json')

    # Check if token file exists
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            from google_auth_oauthlib.flow import InstalledAppFlow
            flow = InstalledAppFlow.from_client_secrets_file(
                credentials_file, SCOPES)
            creds = flow.run_local_server(port=8000)

        # Save the credentials for the next run
        with open(token_path, 'w') as token:
            token.write(creds.to_json())

    return creds


def create_calendar_event(start_time, end_time, summary, description, location, doctor_email):
    credentials = get_credentials()
    service = build('calendar', 'v3', credentials=credentials)

    event = {
        'summary': summary,
        'description': description,
        'start': {
            'dateTime': start_time.isoformat(),
            'timeZone': 'Asia/Kolkata',
        },
        'end': {
            'dateTime': end_time.isoformat(),
            'timeZone': 'Asia/Kolkata',
        },
        'location': location,
        'attendees': [
            {'email': doctor_email},
        ],
    }

    event = service.events().insert(calendarId='primary', body=event).execute()
    return event.get('htmlLink')
