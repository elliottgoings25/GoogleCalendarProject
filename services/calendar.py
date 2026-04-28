import os
import pickle
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

#-------------------------
# Google Calendar Scope
#-------------------------
SCOPES = ['https://www.googleapis.com/auth/calendar.events']

def get_calendar_service():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as f:
            creds = pickle.load(f)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES
            )
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as f:
            pickle.dump(creds, f)
    return build('calendar', 'v3', credentials=creds)


#-------------------------
# ACTION: post event
#-------------------------
def post_event(summary, start_datetime, end_datetime, description='', timezone='America/Chicago'):
    # -----Get calendar service-----
    try:
        service = get_calendar_service()
        
        event = {
            'summary': summary,
            'description': description,
            'start': {'dateTime': start_datetime, 'timeZone': timezone},
            'end': {'dateTime': end_datetime, 'timeZone': timezone},
        }
        
        created = service.events().insert(calendarId='primary', body=event).execute()
        return created
    
    # -----Error handling-----
    except Exception as e:
        print(f"Error posting event: {e}")
        return None