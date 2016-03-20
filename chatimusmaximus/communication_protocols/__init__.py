import chatimusmaximus.communication_protocols as ccp # flake8: noqa

from ccp.xmpp import ReadOnlyXMPPBot
from ccp.socket_io import ReadOnlyWebSocket
from ccp.irc import (create_irc_bot,
                     EchoToMessage)

try:
    from ccp.javascript_webscraper import JavascriptWebscraper
except ImportError:
    pass


__all__ = ['ReadOnlyXMPPBot',
           'ReadOnlyWebSocket',
           'create_irc_bot',
           'EchoToMessage']

if JavascriptWebscraper:
    __all__.append('JavascriptWebscraper')
