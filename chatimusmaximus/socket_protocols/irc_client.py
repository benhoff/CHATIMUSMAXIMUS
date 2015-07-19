import irc3
import threading

from PyQt5 import QtCore
from irc3.plugins.command import command
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

    @command(permission='view')
    def echo(self, mask, target, args):
        print(' '.join(args['<words>']))
        self.chat_signal.emit(mask.nick, ' '.join(args['<words>']), gui.StatusBarSelector.Twitch.value)

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
                   host='irc.twitch.tv', port=6667, realname=None):

    if realname is None:
        realname = nick
    _config['nick'] = nick
    _config['password'] = 'oauth:{}'.format(password)
    _config['host'] = host
    _config['port'] = port
    _config['realname'] = realname

    bot = irc3.IrcBot.from_config(_config)

    return bot
