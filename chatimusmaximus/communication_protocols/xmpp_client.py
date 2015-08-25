import os
import sys
import asyncio
from queue import Queue, Empty
import logging
logging.basicConfig(level=logging.ERROR)

import sleekxmpp

import gui

def fake_verify(*args):
    return

# monkey patch to fix issues with either livecode or 
# sleekxmpp. hard to tell where the problem is
sleekxmpp.xmlstream.cert.verify = fake_verify

class ReadOnlyXMPPBot(sleekxmpp.ClientXMPP):
    def __init__(self,
                 jid,
                 password,
                 message_function=None,
                 room='{user}@chat.livecoding.tv',
                 nick='ReadOnlyBot'):
        
        # Initialize the parent class
        super(ReadOnlyXMPPBot, self).__init__(jid, password)

        # if the there's a format option in the room, add in the user
        if room[0:5] == '{user}':
            room = room.format(jid.user)

        self.room = room
        self.nick = nick

        # One-shot helper method used to register all the plugins
        self._register_plugin_helper() 

        self.add_event_handler("session_start", self.start)
        self.add_event_handler("groupchat_message", self.muc_message)
        self.message_function = message_function

    def _register_plugin_helper(self):
        """
        One-shot helper method used to register all the plugins
        """
        self.register_plugin('xep_0030') # Service Discovery
        self.register_plugin('xep_0004') # Data Forms
        self.register_plugin('xep_0060') # PubSub

        # XMPP Ping
        self.register_plugin('xep_0199', 
                             {'keepalive': True, 'frequency': 60})

        self.register_plugin('xep_0045') # MUC

    def start(self, event):
        self.get_roster()
        self.send_presence()
        self.plugin['xep_0045'].joinMUC(self.room,
                                        self.nick)

    def muc_message(self, msg):
        if self.message_function is not None:
            self.message_function(msg['mucnick'], msg['body'])
