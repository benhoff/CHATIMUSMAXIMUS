import logging

import slixmpp 
from slixmpp.xmlstream import XMLStream


def fake_verify(*args):
    return


# slixmpp.xmlstream.cert.verify = fake_verify


class ReadOnlyXMPPBot(slixmpp.ClientXMPP):
    def __init__(self,
                 jid,
                 password,
                 room,
                 nick='EchoBot',
                 plugin=None):

        # Initialize the parent class
        super().__init__(jid, password)

        self.room = room
        self.nick = nick
        self.communication_plugin = plugin
        self.log = logging.getLogger(__file__)

        # One-shot helper method used to register all the plugins
        self._register_plugin_helper()

        self.add_event_handler("session_start", self.start)
        self.add_event_handler("groupchat_message", self.muc_message)
        self.add_event_handler('connected', self._connected)
        self.add_event_handler('disconnected', self._disconnected)

    def _disconnected(self, *args):
        if self.communication_plugin:
            self.communication_plugin.connected_function(False)

    def _connected(self, *args):
        if self.communication_plugin:
            self.communication_plugin.connected_function(True)

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
        if self.communication_plugin:
            self.communication_plugin.message_function(msg['mucnick'],
                                                       msg['body'])
