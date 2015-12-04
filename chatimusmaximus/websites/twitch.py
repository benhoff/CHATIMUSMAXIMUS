import asyncio

from .website_plugin import WebsitePlugin
from communication_protocols import PATHS


class Twitch(WebsitePlugin):
    def __init__(self):
        """
        This class is a convince/internal api wrapper around another plugin
        """
        super().__init__(platform='twitch')

    def activate(self, settings, **kwargs):
        nick = settings['nick']
        channel = settings['channel']
        password = settings['oauth_token']
        host = 'irc.twitch.tv'
        asyncio.ensure_future(self.start_subprocess(PATHS['irc_path'],
                                                    nick,
                                                    password,
                                                    host,
                                                    channel))
