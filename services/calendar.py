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