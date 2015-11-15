import asyncio

from .website_plugin import WebsitePlugin
from communication_protocols import PATHS


class Livecoding(WebsitePlugin):
    # FIXME: migrate to asyncio library
    def __init__(self):
        super().__init__('livecoding')
        self._xmpp_echo = None

    def activate(self, settings):
        # settings_nick = settings['bot_nick']
        # bot_nick = settings_nick if settings_nick != str() else 'EchoBot'
        password = settings['password']
        local = settings['name']
        domain = 'livecoding.tv'
        resource = 'CHATIMUSMAXIMUS'
        room = settings['room']
        """
        if not room:
            room = '{}@chat.livecoding.tv'.format(jid.name)
        """

        asyncio.ensure_future(self.start_subprocess(PATHS['xmpp_path'],
                                                    local,
                                                    domain,
                                                    room,
                                                    resource,
                                                    password))
