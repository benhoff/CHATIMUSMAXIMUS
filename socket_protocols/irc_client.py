import socket
import sys
import os
from threading import Thread
from PyQt5 import QtCore
from utils import Messager

class ReadOnlyIRCBot(QtCore.QObject):
    HOST = 'irc.twitch.tv'
    PLATFORM = 'TWITCH'
    PORT = 6667
    chat_signal = QtCore.pyqtSignal(str, str, str) 

    def __init__(self, channel, nick=None, oauth_token=None, parent=None):
        super(ReadOnlyIRCBot, self).__init__(parent)
        if nick is None:
            nick = channel 
        if oauth_token is None or oauth_token == '':
            oauth_token = os.getenv('TWITCH_KEY')
        self.nick = nick
        self.oauth_token = oauth_token
        self.channel = channel

        # NOTE: If use `split()` in run this has extra space on the end!!!
        self.connect_message = 'tmi.twitch.tv 376 {} '.format(self.nick)
        self.socket = socket.socket()
        self.readbuffer = ""

        self.socket.connect((self.HOST, self.PORT))

        self.connected = False

        self._thread = Thread(target=self.run)
        self._thread.setDaemon(True)
        self._thread.start()

    def _connect_to_server_helper(self):
        self._send_helper('PASS oauth:{}'.format(self.oauth_token))
        self._send_helper('NICK {}'.format(self.nick))

    def _send_helper(self, message):
        message += '\r\n'
        self.socket.send(bytes(message, 'UTF-8'))

    def run(self):
        self._connect_to_server_helper()
        while True:
            self.readbuffer += self.socket.recv(1024).decode('UTF-8')

            temp = self.readbuffer.split('\n')
            self.readbuffer = temp.pop()

            # For DEBUGGING
            #print('length of temp: ', len(temp))
            for line in temp:
                line = line.rstrip()

                # TODO: switch back to using just `split()`
                line = line.split(':', 2)
                
                # Handles PING/PONG of server
                if line[0] == "PING":
                    # TODO: verify that this works other places than just in my head
                    self._send_helper('PONG {}'.format(line[1]))
                    break
                # Handles the connection method
                elif line[1] == self.connect_message:
                    self.connected = True
                    self._send_helper('JOIN #{}'.format(self.channel))
                    break

                # FIXME: Is there an option where there isn't an item in index of 1?
                # code will break if so...
                try:
                    test_line = line[1].split()
                    if len(test_line) > 0:
                        if test_line[1] == 'PRIVMSG':
                            if len(line) > 1:
                                message = line[2]
                            else:
                                message = 'PLACEHOLDER'
                            self.chat_signal.emit(test_line[0], message, self.PLATFORM)
                            break
                        
                except:
                    print("Unexpected error:", sys.exc_info()[0])
                    print('Line: ', line[1])
                    print(test_line)

                for index, i in enumerate(line):
                    print(line[index])

if __name__ == '__main__':
    irc_bot = ReadOnlyIRCBot('beohoff', nick='beohoff')
    # FIXME: Add in a loop here or something
