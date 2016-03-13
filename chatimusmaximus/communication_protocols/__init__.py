import os

from communication_protocols.xmpp_client import ReadOnlyXMPPBot
from communication_protocols.socket_io_client import ReadOnlyWebSocket
from communication_protocols.irc_client import create_irc_bot, EchoToMessage
try:
    from communication_protocols.javascript_webscraper import JavascriptWebscraper
except ImportError:
    pass


__all__ = ['ReadOnlyXMPPBot',
           'ReadOnlyWebSocket',
           'create_irc_bot',
           'EchoToMessage']

if JavascriptWebscraper:
    __all__.append('JavascriptWebscraper')

