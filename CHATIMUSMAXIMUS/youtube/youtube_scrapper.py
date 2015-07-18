import sys
import os

from time import sleep
from threading import Thread

from selenium import webdriver

from PyQt5 import QtCore
import gui

class YoutubeScrapper(QtCore.QObject):
    chat_signal = QtCore.pyqtSignal(str, str, int)

    def __init__(self, video_url=None, parent=None):
        super(YoutubeScrapper, self).__init__(parent)
        if video_url is None or video_url == str():
            #video_url = get_current_youtube_link()
            video_url = os.getenv('YOUTUBE_URL')

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
                    self.chat_signal.emit(author, 
                                          message,
                                          gui.StatusBarSelector.Youtube.value)
