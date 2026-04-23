import sys
import os
import pickle

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ['https://www.googleapis.com/auth/calendar.events']

def generate_token():
    try:
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
        
        with open('token.pickle', 'wb') as f:
            pickle.dump(creds, f)
        
        print("Token generated successfully!")
        return True
    except Exception as e:
        print(f"Error generating token: {e}")
        return False

if __name__ == '__main__':
    generate_token()