import irc3
import threading

from PyQt5 import QtCore
from irc3.plugins.command import command
from gui import StatusBarSelector
from utils import Messager

@irc3.plugin
class EchoToMessage(object):
    requires = [
            'irc3.plugins.core',
            'irc3.plugins.command'
            ]

    def __init__(self, bot):
        self.bot = bot
        self._messager = Messager()
        self.chat_signal = self._messager.chat_signal

    @irc3.event(irc3.rfc.PRIVMSG)
    def message(self, mask, event, target, data):
        nick = mask.split('!')[0]
        message = data
        self.chat_signal.emit(nick, message, StatusBarSelector.Twitch.value)

_config = dict(
        ssl=False,
        includes=[
            'irc3.plugins.core',
            'irc3.plugins.command',
            'irc3.plugins.human',
            'irc3.plugins.log',
            'irc3.plugins.autojoins',
            __name__,
            ]
        )

def create_irc_bot(nick, password,
                   host=None, 
                   port=6667, realname=None,
                   channel=None):

    if realname is None:
        realname = nick
    if channel is None:
        channel = nick
    _config['nick'] = nick
    _config['password'] = password 
    _config['host'] = host
    _config['port'] = port
    _config['realname'] = realname
    _config['autojoins'] = channel

    bot = irc3.IrcBot.from_config(_config)

    return bot
