### 4/2020 Nicholas A. Gabriel
from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

import base64
import email
from apiclient import errors
from bs4 import BeautifulSoup
import wget
import time

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def credentials():
    """Initialize gmail API with code stolen from google
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return creds

def get_messages(creds,query,maxResults):
    """Get messages obtained by searching query
    """

    service = build('gmail', 'v1', credentials=creds)
    response = service.users().messages().list(userId='me', 
                                               labelIds = ['INBOX'],
                                                q = query,
                                                maxResults=maxResults).execute()
    messages = []
    if 'messages' in response:
        messages.extend(response['messages'])
    while 'nextPageToken' in response:
        page_token = response['nextPageToken']
        response = service.users().messages().list(userId='me',
                                                   labelIds=['INBOX'],
                                                   q = query,
                                                   maxResults=maxResults,
                                                   pageToken=page_token).execute()
        messages.extend(response['messages'])

    print("%i messages fetched" %(len(messages)) )

    return messages

def ct_message_download(messages):

    service = build('gmail', 'v1', credentials=creds)
    n = len(messages)
    counter = range(1,n+1)
    for message,i in zip(messages,counter):
        try:
            msg_str = message_str(message,service)
            soup = BeautifulSoup(msg_str, 'html.parser')
            url = soup.a.get('href')
            wget.download(url, out='ctfiles')
            print("%i/%i files downloaded" %(i,len(messages)))
        except:
          print("%i/%i failed" %(i,len(messages)))

def message_str(message,service):
  
    msg = service.users().messages().get(userId='me',id=message['id'],format='raw').execute()
    msg_str = base64.urlsafe_b64decode(msg['raw'].encode('ASCII'))
    msg_str = msg_str.decode('utf-8')

    return msg_str    

if __name__ == '__main__':
    creds = credentials()
    query = 'from:feedback@crowdtangle.com crowdtangle "Data Download Request" after:04/01/2020'
    maxResults = 500
    messages = get_messages(creds,query,maxResults)
    ct_message_download(messages)