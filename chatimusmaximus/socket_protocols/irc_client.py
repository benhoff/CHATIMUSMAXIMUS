import irc3
import threading
from socket_protocols import EchoToMessage

_config = dict(
        ssl=False,
        includes=[
            'irc3.plugins.core',
            'irc3.plugins.autojoins',
            EchoToMessage,
            __name__,
            ]
        )

def create_irc_bot(channel, password, nick=None, 
                   host='irc.twitch.tv', port=6667, realname=None):
    if nick is None or nick == str():
        nick = channel
    if realname is None:
        realname = nick
    _config['nick'] = nick
    _config['password'] = password
    _config['host'] = host
    _config['port'] = port
    _config['realname'] = realname

    bot = irc3.IrcBot.from_config(_config)

    return bot
