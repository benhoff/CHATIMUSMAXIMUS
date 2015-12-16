import os

from communication_protocols.xmpp_client import ReadOnlyXMPPBot
from communication_protocols.javascript_webscraper import JavascriptWebscraper
from communication_protocols.socket_io_client import ReadOnlyWebSocket
from communication_protocols.irc_client import create_irc_bot, EchoToMessage

_file_path = os.path.abspath(os.path.dirname(__file__))

PATHS = {'xmpp_path': os.path.join(_file_path, 'xmpp_client.py'),
         'javascript_path': os.path.join(_file_path,
                                         'javascript_webscraper.py'),
         'socket_path': os.path.join(_file_path, 'socket_io_client.py'),
         'irc_path': os.path.join(_file_path, 'irc_client.py')}


__all__ = ['ReadOnlyXMPPBot',
           'JavascriptWebscraper',
           'ReadOnlyWebSocket',
           'create_irc_bot',
           'EchoToMessage',
           'PATHS']
