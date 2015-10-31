import asyncio
import sleekxmpp

from .website_plugin import WebsitePlugin
from communication_protocols import ReadOnlyXMPPBot

class LivecodingPlugin(IPlugin):
    # FIXME: migrate to asyncio library
    def __init__(self, settings):
        super().__init__('livecoding')


        jid = sleekxmpp.JID(local=settings['name'], 
                            domain='livecoding.tv', 
                            resource='CHATIMUSMAXIMUS')

        self._livecode = ReadOnlyXMPPBot(jid, password, nick=bot_nick)
        self._livecode.connect()
        loop = asyncio.get_event_loop()
        loop.run_in_executor(None, self._livecode.process)

    def activate(self, settings):
        setting_nick = settings['bot_nick']
        bot_nick = settings_nick if settings_nick != str() else 'EchoBot'
        password = settings['password']

        jid = sleekxmpp.JID(local=settings['name'],
                            domain='livecoding.tv',
                            resource='CHATIMUSMAXIMUS')

        self._xmpp_echo = ReadOnlyXMPPBot(jid, password, nick=bot_nick)
        loop = asyncio.get_event_loop()
        loop.run_in_executor(None, self._xmpp_echo.start_echo)

