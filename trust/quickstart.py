from __future__ import print_function

import base64
import os.path
import time

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']
RETRY_TIME = 1


def get_service(inc):
    """
    Производит аутентификацию и предоставляет сервис для дальнейшей обработки.
    """
    creds = None
    if os.path.exists(f'token_{inc}.json'):
        creds = Credentials.from_authorized_user_file(f'token_{inc}.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                f'credentials_{inc}.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(f'token_{inc}.json', 'w') as token:
            token.write(creds.to_json())
    try:
        # Call the Gmail API
        service = build('gmail', 'v1', credentials=creds)
        return service
    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f'An error occurred: {error}')


def search_messages(service, user_id='me'):
    ''' Поиск непрочитанных сообщений '''
    time.sleep(RETRY_TIME)
    try:
        search_id = service.users().messages().list(userId=user_id, q='label:unread').execute()
        number_results = search_id['resultSizeEstimate']
        final_list = []
        if number_results > 0:
            message_ids = search_id['messages']
            for ids in message_ids:
                final_list.append(ids['id'])
                service.users().messages().batchModify(
                    userId=user_id,
                    body={
                        'ids': ids['id'],
                        'removeLabelIds': ['UNREAD']
                    }
                ).execute()
            return final_list
        else:
            print('Письма не найдены.')
            return False
            
    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f'An error occurred: {error}')


def get_link_message(service, user_id, msg_id):
    try:
        message = service.users().messages().get(userId=user_id, id=msg_id,
                                                format='full').execute()
        playload = message['payload']
        parts = playload.get("parts")   
        for part in parts:
            body = part.get("parts")
        data = body[0].get("body").get("data")
        msg_data = base64.urlsafe_b64decode(data.encode("utf-8")).decode("utf-8")
        msg_lists = msg_data.split('<br />')
        links_data = []
        for list in msg_lists:
            if list.startswith('<a href='):
                links_data.append(list.split('"')[1])
        return links_data
    except Exception as error:
        print('An error occurred: %s' % error)


def main(inc):    
    msg_ids = search_messages(get_service(inc))
    while msg_ids==False:
        msg_ids = search_messages(get_service(inc))
    #print(get_link_message(get_service(), 'me', msg_ids[0]))
    result = []
    if len(msg_ids) > 1:
        for i in range(len(msg_ids)):
            result += get_link_message(get_service(inc), 'me', msg_ids[0])
        return result
    return get_link_message(get_service(inc), 'me', msg_ids[0])


if __name__ == '__main__':
    main(7)
    
