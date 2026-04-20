import os
import pickle
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

#-----Google Calendar Scope and setup-----
SCOPES = ['https://www.googleapis.com/auth/calendar.events']

def get_calendar_service():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as f:
            creds = pickle.load(f)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        with open('token.pickle', 'wb') as f:
            pickle.dump(creds, f)
    return build('calendar', 'v3', credentials=creds)

def post_event(summary, start_datetime, end_datetime, description='', timezone='America/Chicago'):
    """
    Post an event to Google Calendar
    """
    service = get_calendar_service()
    
    event = {
        'summary': summary,
        'description': description,  # 👈 Add this
        'start': {'dateTime': start_datetime, 'timeZone': timezone},
        'end': {'dateTime': end_datetime, 'timeZone': timezone},
    }
    
    created = service.events().insert(calendarId='primary', body=event).execute()
    return created