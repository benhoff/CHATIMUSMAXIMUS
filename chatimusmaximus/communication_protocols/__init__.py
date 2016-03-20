from chatimusmaximus.communication_protocols.xmpp import ReadOnlyXMPPBot
from chatimusmaximus.communication_protocols.socket_io import ReadOnlyWebSocket
from chatimusmaximus.communication_protocols.irc import (create_irc_bot,
                                                         EchoToMessage)

try:
    from chatimusmaximus.communication_protocols.javascript_webscraper import JavascriptWebscraper # flake8: noqa
except ImportError:
    pass


__all__ = ['ReadOnlyXMPPBot',
           'ReadOnlyWebSocket',
           'create_irc_bot',
           'EchoToMessage']

if JavascriptWebscraper:
    __all__.append('JavascriptWebscraper')
