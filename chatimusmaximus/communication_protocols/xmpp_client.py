import os
import sys
import logging
logging.basicConfig(level=logging.ERROR)

from threading import Thread
import sleekxmpp

from utils import Messager
import gui

def fake_verify(*args):
    return

# monkey patch to fix issues with either livecode or 
# sleekxmpp. hard to tell where the problem is
sleekxmpp.xmlstream.cert.verify = fake_verify

class ReadOnlyXMPPBot(sleekxmpp.ClientXMPP):
    def __init__(self, jid, password, room=None, nick='ReadOnlyBot'):
        super(ReadOnlyXMPPBot, self).__init__(jid, password)
        if room is None:
            # FIXME: remove the livecoding reference
            room = '{user}@chat.livecoding.tv'.format(jid.user)
        self.room = room
        self.nick = nick
        self._register_plugin_helper() 

        self.add_event_handler("session_start", self.start, threaded=True)
        self.add_event_handler("groupchat_message", self.muc_message)

        # use the trivial instance `_messager` to get around multiple inheritance
        # problems with PyQt
        self._messager = Messager()
        # Duck type the `chat_signal` onto the `Socket` instance/class
        self.chat_signal = self._messager.chat_signal

    def _register_plugin_helper(self):
        self.register_plugin('xep_0030') # Service Discovery
        self.register_plugin('xep_0004') # Data Forms
        self.register_plugin('xep_0060') # PubSub
        self.register_plugin('xep_0199', {'keepalive': True, 'frequency': 60}) # XMPP Ping
        self.register_plugin('xep_0045') # MUC

    def start(self, event):
        self.get_roster()
        self.send_presence()
        self.plugin['xep_0045'].joinMUC(self.room,
                                        self.nick,
                                        wait=True)

    def muc_message(self, msg):
        self._messager.recieve_chat_data(msg['mucnick'], 
                                         msg['body'], 
                                         gui.StatusBarSelector.Livecoding.value)
