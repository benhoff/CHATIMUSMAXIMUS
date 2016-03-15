import logging
import argparse
import sleekxmpp
from time import sleep

import zmq

from chatimusmaximus.communication_protocols._messaging import ZmqMessaging


class ReadOnlyXMPPBot(sleekxmpp.ClientXMPP):
    def __init__(self,
                 jid,
                 password,
                 room,
                 nick='EchoBot',
                 pub_address='tcp://127.0.0.1:6001',
                 service_name=''):

        # Initialize the parent class
        super().__init__(jid, password)
        self.messaging = ZmqMessaging(service_name, pub_address)

        self.room = room
        self.nick = nick
        self.log = logging.getLogger(__file__)

        # One-shot helper method used to register all the plugins
        self._register_plugin_helper()

        self.add_event_handler("session_start", self.start)
        self.add_event_handler("groupchat_message", self.muc_message)
        self.add_event_handler('connected', self._connected)
        self.add_event_handler('disconnected', self._disconnected)

    def _disconnected(self, *args):
        self.messaging.send_message('DISCONNECTED')

    def _connected(self, *args):
        self.messaging.send_message('CONNECTED')

    def process(self):
        self.init_plugins()
        super().process()

    def _register_plugin_helper(self):
        """
        One-shot helper method used to register all the plugins
        """
        # Service Discovery
        self.register_plugin('xep_0030')
        # XMPP Ping
        self.register_plugin('xep_0199')
        # Multiple User Chatroom
        self.register_plugin('xep_0045')

    def start(self, event):
        self.log.info('starting xmpp')
        self.send_presence()
        self.plugin['xep_0045'].joinMUC(self.room,
                                        self.nick)
        self.get_roster()

    def muc_message(self, msg):
        self.messaging.send_message('MSG',
                                    msg['mucnick'],
                                    msg['body'])


def _get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('local', help='local arg for string parsing')
    parser.add_argument('domain', help='domain for xmpp')
    parser.add_argument('room', help='room!')
    parser.add_argument('resource', help='resource')
    parser.add_argument('password', help='password')
    parser.add_argument('service_name')
    parser.add_argument('--pub_address', default='tcp://127.0.0.1:6001')
    parser.add_argument('--nick', default='EchoBot')

    return parser.parse_args()


def main():
    args = _get_args()
    jid = '{}@{}/{}'.format(args.local, args.domain, args.resource)

    xmpp_bot = ReadOnlyXMPPBot(jid,
                               args.password,
                               args.room,
                               args.nick,
                               pub_address=args.pub_address,
                               service_name=args.service_name)

    while True:
        try:
            if xmpp_bot.connect():
                xmpp_bot.process(block=True)
            else:
                sleep(3)
        except Exception:
            sleep(3)

if __name__ == '__main__':
    main()
