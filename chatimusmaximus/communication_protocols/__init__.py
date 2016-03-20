from chatimusmaximus.communication_protocols.xmpp import ReadOnlyXMPPBot
from chatimusmaximus.communication_protocols.socket_io import ReadOnlyWebSocket
from chatimusmaximus.communication_protocols.irc import (create_irc_bot,
                                                         EchoToMessage)

__all__ = ['ReadOnlyXMPPBot',
           'ReadOnlyWebSocket',
           'create_irc_bot',
           'EchoToMessage']
try:
    from chatimusmaximus.communication_protocols.javascript_webscraper import JavascriptWebscraper # flake8: noqa
    __all__.append('JavascriptWebscraper')
except ImportError:
    pass
