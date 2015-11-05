import logging
import argparse
import slixmpp


class ReadOnlyXMPPBot(slixmpp.ClientXMPP):
    def __init__(self,
                 jid,
                 password,
                 room,
                 nick='EchoBot'):

        # Initialize the parent class
        super().__init__(jid, password)

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
        print('DISCONNECTED')

    def _connected(self, *args):
        print('CONNECTED')

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
        print('MSG NICK: {} BODY: {}'.format(msg['mucnick'],
                                             msg['body']))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('local', help='local arg for string parsing')
    parser.add_argument('domain', help='domain for xmpp')
    parser.add_argument('room', help='room!')
    parser.add_argument('resource', help='resource')
    parser.add_argument('password', help='password')
    args = parser.parse_args()
    jid = '{}@{}/{}'.format(args.local, args.domain, args.resource)
    # jid = slixmpp.JID(jid)

    xmpp_bot = ReadOnlyXMPPBot(jid, args.password, args.room)
    xmpp_bot.connect()
    xmpp_bot.process()

if __name__ == '__main__':
    main()
