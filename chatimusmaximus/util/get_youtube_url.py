import os
import sys
import httplib2

from apiclient.discovery import build
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import run_flow, argparser

_YOUTUBE_API_SERVICE_NAME = 'youtube'
_YOUTUBE_API_VERSION = 'v3'


def _youtube_authentication(client_filepath):
    youtube_scope = "https://www.googleapis.com/auth/youtube.readonly"
    missing_client_message = "You need to populate the client_secrets.json!"
    flow = flow_from_clientsecrets(client_filepath,
                                   scope=youtube_scope,
                                   message=missing_client_message)
    filepath = "{}-oauth2.json".format(sys.argv[0])
    if os.path.isfile(filepath):
        os.remove(filepath)

    storage = Storage(filepath)
    credentials = storage.get()
    if credentials is None or credentials.invalid:
        credentials = run_flow(flow, storage, argparser.parse_args())
        return build(_YOUTUBE_API_SERVICE_NAME,
                     _YOUTUBE_API_VERSION,
                     http=credentials.authorize(httplib2.Http()))


def get_current_youtube_link(client_secrets_filepath):
    youtube_api = _youtube_authentication(client_secrets_filepath)
    parts = 'id, snippet, status'
    livestream_requests = youtube_api.liveBroadcasts().list(mine=True,
                                                         part=parts,
                                                         maxResults=5)

    while livestream_requests:
        response = livestream_requests.execute()
        # TODO: add better parsing here
        youtube_id = response.get('items', [])[0]['id']
        return 'http://youtube.com/watch?v={}'.format(youtube_id)
