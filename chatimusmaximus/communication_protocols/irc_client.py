import irc3
from irc3.plugins.autojoins import AutoJoins
import threading

from PyQt5 import QtCore
from irc3.plugins.command import command
from gui import MainWindow

@irc3.plugin
class AutoJoinMessage(AutoJoins):
    requires = [
            'irc3.plugins.core',
            ]

    def __init__(self, bot):
        super(AutoJoinMessage, self).__init__(bot)
        self.plugin = self.bot.config.get('plugin', None)

    def connection_lost(self):
        if self.plugin is not None:
            self.plugin.connected_function(False)
        super(AutoJoinMessage, self).connection_lost()

    def join(self, channel=None):
        super(AutoJoinMessage, self).join(channel)
        if self.plugin is not None:
            self.plugin.connected_function(True)

    @irc3.event(irc3.rfc.KICK)
    def on_kick(self, mask, channel, target, **kwargs):
        if self.plugin is not None:
            self.plugin.connected_function(False)
        super(AutoJoinMessage, self).on_kick(mask, channel, target, **kwargs)

    @irc3.event("^:\S+ 47[1234567] \S+ (?P<channel>\S+).*")
    def on_err_join(self, channel, **kwargs):
        if self.plugin is not None:
            self.plugin.connected_function(False)
        super(AutoJoinMessage, self).on_err_join(channel, **kwargs)

@irc3.plugin
class EchoToMessage(object):
    requires = [
            'irc3.plugins.core',
            'irc3.plugins.command'
            ]

    def __init__(self, bot):
        self.bot = bot
        self.plugin = self.bot.config.get('plugin', None)


    @irc3.event(irc3.rfc.PRIVMSG)
    def message(self, mask, event, target, data):
        nick = mask.split('!')[0]
        message = data
        if self.plugin is not None:
            self.plugin.message_function(nick, message)


def create_irc_bot(nick, 
                   password,
                   host=None, 
                   port=6667, 
                   realname=None,
                   channel=None,
                   plugin=None):

    config = dict(
            ssl=False,
            includes=[
                'irc3.plugins.core',
                'irc3.plugins.command',
                'irc3.plugins.human',
                'irc3.plugins.log',
                __name__,
                ]
            )
    if realname is None:
        realname = nick
    if channel is None:
        channel = nick
    config['nick'] = nick
    config['password'] = password 
    config['host'] = host
    config['port'] = port
    config['realname'] = realname
    config['autojoins'] = channel
    config['plugin'] = plugin

    bot = irc3.IrcBot.from_config(config)

    return bot
