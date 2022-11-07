from __future__ import print_function
import os
import base64
import os.path
from email.message import EmailMessage
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow

# Gmail access scopes
SCOPES = ['https://mail.google.com/', 'https://www.googleapis.com/auth/gmail.readonly',
          'https://www.googleapis.com/auth/gmail.modify', 'https://www.googleapis.com/auth/gmail.metadata']


# Lambda handler function
def handler(event, context):
    print('Handler called')
    user_email = event['user_email']
    username = event['username']

    # Run once to authorise and login
    # authorise_and_login()

    send_email(user_email, username)
    return 'Email sent!'


# Send email
def send_email(user_email, username):

    creds = Credentials.from_authorized_user_file('token.json')

    email_content = f'''
Hi {username},

From our team at Shiny Spoon, we would like to welcome you to SS. If you have any inquiries, please reply to this email, and we'll get back to you as soon as possible.
        
Kind regards
Shiny Spoon
    '''

    try:
        service = build('gmail', 'v1', credentials=creds)
        message = EmailMessage()

        message.set_content(email_content)

        message['To'] = user_email
        message['From'] = os.getenv('SS_EMAIL')
        message['Subject'] = 'Welcome to Shiny Spoon :)'

        # encoded message
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()) \
            .decode()

        create_message = {
            'raw': encoded_message
        }
        # pylint: disable=E1101
        send_message = (service.users().messages().send
                        (userId="me", body=create_message).execute())
        print(F'Message Id: {send_message["id"]}')
    except HttpError as error:
        print(F'An error occurred: {error}')
        send_message = None
    return send_message


# Authorise and login to gmail account
def authorise_and_login():
    creds = None

    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'shiny_spoon_gmail_client.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        # Call the Gmail API
        service = build('gmail', 'v1', credentials=creds)
        results = service.users().labels().list(userId='me').execute()
        labels = results.get('labels', [])

        if not labels:
            print('No labels found.')
            return
        print('Labels:')
        for label in labels:
            print(label['name'])

    except HttpError as error:
        print(f'An error occurred: {error}')
