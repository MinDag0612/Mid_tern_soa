from __future__ import print_function
import os.path
import base64
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from email.message import EmailMessage
from email.utils import formataddr
from datetime import datetime
from fastapi import APIRouter, Depends
from schemas.mail_schema import mail

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/gmail.send',
          'https://www.googleapis.com/auth/gmail.compose']


def send_email_v1(recipient, subject=None, content=None, port=0):
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials_desktop_apps.json', SCOPES)
            creds = flow.run_local_server(port=port)  # https://dhpit.com/go/f5kizi

        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    # Call Gmail API
    try:
        # Call the Gmail API
        service = build('gmail', 'v1', credentials=creds)

        # Prepare a message
        message = EmailMessage()
        if subject is not None:
            message['Subject'] = str(subject)
        else:
            message['Subject'] = 'Test Message (' + str(datetime.now().strftime('%m/%d/%Y %H:%M:%S')) + ')'

        if content is not None:
            message.set_content(str(content))
        else:
            message.set_content('This is a test message sent from a Flask application.')

        message['To'] = recipient  # you should validate email address format
        message['From'] = formataddr(('Flask App', service.users().getProfile(userId='me').execute()['emailAddress']))

        # encoded message
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

        create_message = {
            'raw': encoded_message
        }

        send_message = service.users().messages().send(userId="me", body=create_message).execute()
        return True
    except HttpError as e:
        print(f'Error occurred: {e}')
        return False

# send_email_v1("523h0011@student.tdtu.edu.vn", "111", "111")
mailler_router = APIRouter()

@mailler_router.get("/")
def test():
    return "Mailler sucesss"

@mailler_router.post("/send-mail")
def send_mail(mail: mail):
    sended_mail = send_email_v1(mail.recipient, mail.subject, mail.content)
    if (sended_mail):
        return {"message": f"Mail --{mail.subject}-- was send"}
    return {"message": f"Can not send --{mail.subject}--"}