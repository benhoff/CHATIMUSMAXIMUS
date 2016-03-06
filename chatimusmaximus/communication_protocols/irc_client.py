import sys
import argparse

import zmq
import irc3
from irc3.plugins.autojoins import AutoJoins


@irc3.plugin
class AutoJoinMessage(AutoJoins):
    requires = ['irc3.plugins.core', ]

    def __init__(self, bot):
        super().__init__(bot)
        context = zmq.Context()
        self.bot.pub_socket = context.socket(zmq.PUB)
        self.socket.bind(bot.config.pub_address)
        self.bot._service_name = bot.config.service_name.encode('ascii')

    def connection_lost(self):
        frame = (self.bot._service_name,
                 b'DISCONNECTED')
        self.bot.pub_socket.send_multipart(frame)
        super(AutoJoinMessage, self).connection_lost()

    def join(self, channel=None):
        super(AutoJoinMessage, self).join(channel)
        frame = (self.bot._service_name,
                 b'CONNECTED')
        self.bot.pub_socket.send_multipart(frame)

    @irc3.event(irc3.rfc.KICK)
    def on_kick(self, mask, channel, target, **kwargs):
        frame = (self.bot._service_name,
                 b'DISCONNECTED')
        self.bot.pub_socket.send_multipart(frame)
        super().on_kick(mask, channel, target, **kwargs)

    @irc3.event("^:\S+ 47[1234567] \S+ (?P<channel>\S+).*")
    def on_err_join(self, channel, **kwargs):
        frame = (self.bot._service_name,
                 b'DISCONNECTED')
        self.bot.pub_socket.send_multipart(frame)
        super().on_err_join(channel, **kwargs)


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
        frame = (self.bot._service_name,
                 b'MSG',
                 nick,
                 message)
        self.bot.pub_socket.send_multipart(frame)


def create_irc_bot(nick,
                   password,
                   host=None,
                   port=6667,
                   realname=None,
                   channel=None,
                   pub_address='',
                   service_name=''):

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
    config['service_name'] = service_name
    config['pub_address'] = pub_address

    bot = irc3.IrcBot.from_config(config)

    return bot

def main(nick, password, host, channel):
    irc_client = create_irc_bot(nick,
                                password,
                                host,
                                channel=channel)

    irc_client.create_connection()
    irc_client.add_signal_handlers()
    event_loop = asyncio.get_event_loop()
    try:
        event_loop.run_forever()
    except KeyboardInterrupt:
        pass
    event_loop.close()
    sys.exit()

def _get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('nick')
    parser.add_argument('password')
    parser.add_argument('host')
    parser.add_argument('channel')
    parser.add_argument('pub_address')
    parser.add_argument('service_name')

    return parser.parse_args()


if __name__ == '__main__':

    args = _get_args()

    main(args.nick,
         args.password,
         args.host,
         args.channel,
         args.pub_address,
         args.service_name)
