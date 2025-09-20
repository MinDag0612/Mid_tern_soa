from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.send',
    'https://www.googleapis.com/auth/gmail.compose'
]

flow = InstalledAppFlow.from_client_secrets_file('credentials_desktop_apps.json', SCOPES)
creds = flow.run_local_server(port=0)   # sẽ mở trình duyệt trên máy host
with open('token.json', 'w') as token:
    token.write(creds.to_json())
