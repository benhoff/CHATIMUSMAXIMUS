import os
import sys
import httplib2

from apiclient.discovery import build
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow

_YOUTUBE_API_SERVICE_NAME = 'youtube'
_YOUTUBE_API_VERSION = 'v3'

def _youtube_authentication():
    client_secrets_file = 'client_secrets.json'
    client_secrets_file = os.path.abspath(os.path.join(os.getcwd(), 
                                          client_secrets_file))

    youtube_scope = "https://www.googleapis.com/auth/youtube.readonly"
    missing_client_message = "You need to populate the client_secrets.json!"

    flow = flow_from_clientsecrets(client_secrets_file,
            scope=youtube_scope)

    storage = Storage("{}-oauth2.json".format(sys.argv[0]))
    credentials = storage.get()

    if credentials is None or credentials.invalid:
        credentials = run_flow(flow, storage, argparser.parse_args())

    return build(_YOUTUBE_API_SERVICE_NAME, 
                 _YOUTUBE_API_VERSION, 
                 http=credentials.authorize(httplib2.Http()))

def get_current_youtube_link():
    youtube_api = _youtube_authentication()

    broadcasts_requests = youtube_api.liveStreams().list(
            part='id,snippet',
            mine=True,
            maxResults=5)

    while broadcasts_requests:
        response = broadcasts_requests.execute()

        for stream in response.get("items", []):
            print('{} {}'.format(stream['snippet']['title'], stream['id']))

        broadcasts_requests = youtube_api.liveStreams().list_next(broadcasts_requests, response)

    youtube_id = response.get('items', [])[0]['id']

if __name__ == '__main__':
    get_current_youtube_link()
