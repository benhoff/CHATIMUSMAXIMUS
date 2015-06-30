import sys
import os
#import httplib2

from time import sleep
from threading import Thread

from selenium import webdriver

from apiclient.discovery import build
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow

from PyQt5 import QtCore

"""
_YOUTUBE_API_SERVICE_NAME = 'youtube'
_YOUTUBE_API_VERSION = 'v3'

def _youtube_authentication():
    client_secrets_file = 'client_secrets.json'
    youtube_scope = "https://www.googleapis.com/auth/youtube.readonly"
    missing_client_message = "You need to populate the client_secrets.json!"

    flow = flow_from_clientsecrets(client_secrets_file,
            scope=youtube_scope,
            message=missing_client_message)

    storage = Storage("{}-oauth2.json".format(sys.argv[0]))
    credentials = storage.get()

    if credentials is None or credentials.invalid:
        credentials = run_flow(flow, storage, args)

    return build(_YOUTUBE_API_SERVICE_NAME, 
                 _YOUTUBE_API_VERSION, 
                 http=credentials.authorize(httplib2.Http()))

def get_current_youtube_link():
    youtube_api = _youtube_authentication()

    broadcasts_requests = youtube.liveBroadcasts().list(
            broadcastStatus=('active',),
            part='id',
            maxResults=5)

    while broadcasts_requests:
        response = broadcasts_requests.execute()

    youtube_id = response.get('items', [])[0]['id']

    return 'http://youtube.com/watch?v={}'.format(youtube_id)
"""

class YoutubeScrapper(QtCore.QObject):
    chat_signal = QtCore.pyqtSignal(str, str, str)

    def __init__(self, video_url=None, parent=None):
        super(YoutubeScrapper, self).__init__(parent)
        """
        if video_url is None:
            video_url = get_current_youtube_link()
        """

        self.video_url = video_url
        self._number_of_messages = 0

        self._thread = Thread(target=self.run)
        self._thread.setDaemon(True)
        self._thread.start()
    
    def run(self):
        driver = webdriver.PhantomJS()
        # TODO: see if this is needed or not
        driver.set_window_size(1000, 1000)
        driver.get(self.video_url)

        # NOTE: need some time for comments to load
        sleep(5)
        all_comments = driver.find_element_by_id("all-comments")
        comments = all_comments.find_elements_by_tag_name('li')
        self._number_of_messages = len(comments)
        for comment in comments:
            author = comment.find_element_by_class_name('author').text
            message = comment.find_element_by_class_name('comment-text').text

            self.chat_signal.emit(author, message, 'YT')

        while True:
            comments = all_comments.find_elements_by_tag_name('li')
            comments_length = len(comments)

            if comments_length > self._number_of_messages:
                # NOTE: this number is intentionally NEGATIVE
                messages_not_parsed = self._number_of_messages - comments_length

                self._number_of_messages = len(comments)
                comments = comments[messages_not_parsed:]
                for comment in comments:
                    author = comment.find_element_by_class_name('author').text
                    message = comment.find_element_by_class_name('comment-text').text
                    self.chat_signal.emit(author, message, 'YT')

if __name__ == '__main__':
    scrapper = YoutubeScrapper('https://www.youtube.com/watch?v=W2DS6wT6_48')
    while True:
        sleep(1)
