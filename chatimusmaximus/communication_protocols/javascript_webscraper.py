import sys
import os

from time import sleep
from threading import Thread

from selenium import webdriver

from PyQt5 import QtCore
import gui

class JavascriptWebscraper(object):

    def __init__(self, url=None, 
            comment_element_id=None,
            author_class_name=None,
            message_class_name=None,
            message_function=None):

        """
        `comment_element_id` is the css element where all the comments are, 
        i.e., 'all-comments' for youtube 

        `author_class_name` is the css class which holds the comment author username
        i.e., 'yt-user-name' for youtube

        `message_class_name` is the css class which holds the comment test
        ie., 'comment-text' for youtube
        """

        self.url = url
        self._number_of_messages = 0

        self.comment_element_id = comment_element_id
        self.author_class_name = author_class_name
        self.message_class_name = message_class_name
        self.message_function = message_function

        self._thread = Thread(target=self.run)
        self._thread.setDaemon(True)
        self._thread.start()
    
    def run(self):
        driver = webdriver.PhantomJS()
        # TODO: see if this is needed or not
        driver.set_window_size(1000, 1000)
        driver.get(self.url)

        # NOTE: need some time for comments to load
        sleep(5)

        all_comments = driver.find_element_by_id(self.comment_element_id)
        # TODO: add in a signal here that all is connected!

        # NOTE: make sure this is ok if using for anything other than youtube
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
                    author = comment.find_element_by_class_name(
                            self.author_class_name).text

                    message = comment.find_element_by_class_name(
                            self.message_class_name).text

                    if self.message_function is not None:
                        self.message_function(author, message)
