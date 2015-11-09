import sys
import asyncio
import argparse
import irc3
from irc3.plugins.autojoins import AutoJoins


@irc3.plugin
class AutoJoinMessage(AutoJoins):
    requires = ['irc3.plugins.core', ]

    def __init__(self, bot):
        super(AutoJoinMessage, self).__init__(bot)

    def connection_lost(self):
        print('DISCONNECTED')
        super(AutoJoinMessage, self).connection_lost()

    def join(self, channel=None):
        super(AutoJoinMessage, self).join(channel)
        print('CONNECTED')

    @irc3.event(irc3.rfc.KICK)
    def on_kick(self, mask, channel, target, **kwargs):
        print('DISCONNECTED')
        super(AutoJoinMessage, self).on_kick(mask, channel, target, **kwargs)

    @irc3.event("^:\S+ 47[1234567] \S+ (?P<channel>\S+).*")
    def on_err_join(self, channel, **kwargs):
        print('DISCONNECTED')
        super(AutoJoinMessage, self).on_err_join(channel, **kwargs)


@irc3.plugin
class EchoToMessage(object):
    requires = ['irc3.plugins.core',
                'irc3.plugins.command']

    def __init__(self, bot):
        self.bot = bot

    @irc3.event(irc3.rfc.PRIVMSG)
    def message(self, mask, event, target, data):
        nick = mask.split('!')[0]
        message = data
        print('MSG NICK: {} BODY: {}'.format(nick, message))


def create_irc_bot(nick,
                   password,
                   host=None,
                   port=6667,
                   realname=None,
                   channel=None):

    config = dict(ssl=False,
                  includes=['irc3.plugins.core',
                            'irc3.plugins.command',
                            'irc3.plugins.human',
                            'irc3.plugins.log',
                            __name__])

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

    bot = irc3.IrcBot.from_config(config)

    return bot

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('nick')
    parser.add_argument('password')
    parser.add_argument('host')
    parser.add_argument('channel')

    args = parser.parse_args()

    irc_client = create_irc_bot(args.nick, args.password, args.host, channel=args.channel)
    irc_client.create_connection()
    irc_client.add_signal_handlers()
    try:
        asyncio.get_event_loop().run_forever()
    except KeyboradInterrupt:
        pass
    event_loop.close()
    sys.exit()
