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
        irc_client_path = os.path.realpath(os.path.join(os.path.dirname(__file__),
                                                        '..',
                                                        'communication_protocols',
                                                        'irc_client.py'))


        self.process = asyncio.ensure_future(asyncio.create_subprocess_exec(sys.executable,
                                                                            irc_client_path, 
                                                                            nick,
                                                                            password,
                                                                            host,
                                                                            channel))

        asyncio.ensure_future(self._reoccuring())
