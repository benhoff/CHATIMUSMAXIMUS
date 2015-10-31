import sleekxmpp

from .website_plugin import WebsitePlugin
from communication_protocols import ReadOnlyXMPPBot

class Livecoding(WebsitePlugin):
    # FIXME: migrate to asyncio library
    def __init__(self):
        super().__init__('livecoding')
        self._xmpp_echo = None

    def activate(self, settings):
        settings_nick = settings['bot_nick']
        bot_nick = settings_nick if settings_nick != str() else 'EchoBot'
        password = settings['password']

        jid = sleekxmpp.JID(local=settings['name'],
                            domain='livecoding.tv',
                            resource='CHATIMUSMAXIMUS')
        room = settings['room']
        if room == str():
            room = '{}@chat.livecoding.tv'.format(jid.name)

        self._xmpp_echo = ReadOnlyXMPPBot(jid,
                                          password,
                                          room,
                                          nick=bot_nick,
                                          plugin=self)
        self._xmpp_echo.connect()
        self._xmpp_echo.process()
