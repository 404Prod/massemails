# pylint: disable=E1101
"""This module holds all the logic for the mail generation and sending through the Gmail API."""
import base64
import os.path as op
import json

from email.message import EmailMessage
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from requests import HTTPError
import pandas as pd

SCOPES = [
        "https://www.googleapis.com/auth/gmail.send"
    ]

config = {}

def send_mail(creds, mail_to, attachments):
    """This function handles the mail build and send operations"""
    service = build('gmail', 'v1', credentials=creds)

    message = EmailMessage()

    message.set_content(config['mail']['body'])

    if attachments:
        for attachment in attachments:
            with open(attachment, 'rb') as content_file:
                content = content_file.read()
                message.add_attachment(
                    content,
                    maintype='application',
                    subtype=(attachment.split('.')[1]),
                    filename=config['mail']['attachment']
                )

    message['to'] = mail_to
    message['subject'] = config['mail']['subject']
    create_message = {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}

    try:
        message = (service.users().messages().send(userId="me", body=create_message).execute())
        print(f" {message['id']} sent, OK.")
    except HTTPError as error:
        print(f"{error} - KO !!!!")
        message = None

def main(conf):
    """This function handles the main logic"""
    print("MasseMails v0.0.1")

    flow = InstalledAppFlow.from_client_secrets_file(conf['files']['credentials'], SCOPES)
    creds = flow.run_local_server(port=0)

    listing = pd.read_excel(conf['files']['listing'], engine='odf')
    print(f"About to send messages to {len(listing)} customers in listing.")

    for i in range(len(listing)):
        clean_nb = str(listing.iloc[i, 0]).split('.', maxsplit=1)[0]
        dest_email = listing.iloc[i, 1]
        if dest_email is not None:
            if clean_nb != 'nan':
                if op.isfile(f'{conf["folders"]["data"]}/{clean_nb}.jpeg'):
                    print(f'Sending photo {clean_nb}.jpeg to email {dest_email}...', end='')
                    send_mail(
                        creds,
                        dest_email,
                        [
                            str(f'{conf["folders"]["data"]}/{clean_nb}.jpeg')
                        ]
                    )
        else:
            print(f'Line not clean, missing either nb or email or photo {clean_nb} not there. PASS')



if __name__ == "__main__":
    with open('config.json', "r", encoding="utf-8") as jfile:
        config = json.load(jfile)
    main(config)
