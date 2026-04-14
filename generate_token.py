import pickle
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ['https://www.googleapis.com/auth/calendar.events']

flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
creds = flow.run_local_server(port=8080)  #force a specific port

with open('token.pickle', 'wb') as f:
    pickle.dump(creds, f)

print("token.pickle generated successfully!")