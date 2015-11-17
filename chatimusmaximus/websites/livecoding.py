import asyncio

from .website_plugin import WebsitePlugin
from communication_protocols import PATHS


class Livecoding(WebsitePlugin):
    def __init__(self):
        super().__init__('livecoding')
        self._xmpp_echo = None
        self.domain = 'livecoding.tv'
        self.resource = 'CHATIMUSMAXIMUS'

        self.password = None 
        self.local = None 
        self.room = None

    def activate(self, password=None, local=None, room=None):
        # settings_nick = settings['bot_nick']
        # bot_nick = settings_nick if settings_nick != str() else 'EchoBot'
        """
        if not room:
            room = '{}@chat.livecoding.tv'.format(jid.name)
        """
        self.password = password if password
        self.local = local if local
        self.room = room if room

        asyncio.ensure_future(self.start_subprocess(PATHS['xmpp_path'],
                                                    self.local,
                                                    self.domain,
                                                    self.room,
                                                    self.resource,
                                                    self.password))
