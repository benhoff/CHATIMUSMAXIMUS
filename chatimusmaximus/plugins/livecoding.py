# NOTE: Currently unsupported
"""
import asyncio

import sleekxmpp

from plugins import IPlugin
from gui import MainWindow
from utils import Messager
from communication_protocols import ReadOnlyXMPPBot

class LivecodingPlugin(IPlugin):
    # FIXME: migrate to asyncio library
    def __init__(self, settings):
        super(LivecodingPlugin, self).__init__()

        # use the trivial instance `_messager` to get around multiple inheritance
        # problems with PyQt
        self._messager = Messager(MainWindow.StatusBarSelector.Livecoding)
        # Duck type the `chat_signal` onto the `Socket` instance/class
        self.chat_signal = self._messager.chat_signal

        # check to see the user has passed in a bot nick and assign it if so
        bot_nick = settings['bot_nick'] if settings['bot_nick'] != str() else 'ReadOnlyBot'
        password = settings['password'] if settings['password'] != str() else os.getenv('LIVECODE_PASS') 

        jid = sleekxmpp.JID(local=settings['name'], 
                            domain='livecoding.tv', 
                            resource='CHATIMUSMAXIMUS')

        self._livecode = ReadOnlyXMPPBot(jid, password, nick=bot_nick)
        self._livecode.connect()
        loop = asyncio.get_event_loop()
        loop.run_in_executor(None, self._livecode.process)
"""
