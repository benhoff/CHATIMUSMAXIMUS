import os
import sys
import asyncio

from .website_plugin import WebsitePlugin
import communication_protocols


class Twitch(WebsitePlugin):
    def __init__(self):
        """
        This class is a convince/internal api wrapper around another plugin
        """
        super().__init__(platform='twitch')

    def activate(self, settings):
        nick = settings['nick'],
        channel =  settings['channel']
        password = settings['oauth_token'],
        host = 'irc.twitch.tv'
        self.start_subprocess(communication_protocols.PATHS['irc_path'],
                              nick,
                              password,
                              host,
                              channel)
