import asyncio
from queue import Queue, Empty

import sleekxmpp
from sleekxmpp.xmlstream import scheduler

# https://gist.github.com/mborho/55be89eead0b0e19e051
class ReadOnlyXMPPBot(sleekxmpp.ClientXMPP):
    def __init__(self,
                 jid,
                 password,
                 message_function=None,
                 room='{user}@chat.livecoding.tv',
                 nick='ReadOnlyBot'):
        
        # Initialize the parent class
        super().__init__(jid, password)

        # if the there's a format option in the room, add in the user
        if room[0:5] == '{user}':
            room = room.format(jid.user)

        self.room = room
        self.nick = nick
        self.queue = Queue()

        # One-shot helper method used to register all the plugins
        self._register_plugin_helper() 

        self.add_event_handler("session_start", self.start)
        self.add_event_handler("groupchat_message", self.muc_message)

    def _register_plugin_helper(self):
        """
        One-shot helper method used to register all the plugins
        """
        # Service Discovery
        self.register_plugin('xep_0030')
        # XMPP Ping
        self.register_plugin('xep_0199')

        # MUC
        self.register_plugin('xep_0045')

    def from_main_thread_nonblocking(self):
        try:
            msg = self.queue.get(False)
        except Empty:
            pass

    def start(self, event):
        self.send_presence()
        self.plugin['xep_0045'].joinMUC(self.room,
                                        self.nick,
                                        wait=True)

        self.get_roster()
        self.scheduler.add('asyncio_queue',
                           2, 
                           self.from_main_thread_nonblocking,
                           repeat=True,
                           qpointer=self.event_queue)

    def muc_message(self, msg):
        if self.message_function:
            self.message_function(msg['mucnick'], msg['body'])
