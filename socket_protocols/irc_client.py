import socket
import sys
import os
from threading import Thread
from PyQt5 import QtCore
from utils import Messager

class ReadOnlyIRCBot(QtCore.QObject):
    HOST = 'irc.twitch.tv'
    PLATFORM = 'Twitch'
    PORT = 6667
    chat_signal = QtCore.pyqtSignal(str, str, str) 

    def __init__(self, channel, nick=None, oauth_token=None, parent=None):
        super(ReadOnlyIRCBot, self).__init__(parent)
        if nick is None:
            nick = channel 
        if oauth_token is None or oauth_token == '':
            oauth_token = os.getenv('TWITCH_KEY')
            if not oauth_token:
                print("No twitch OAUTH token found :(")

        self.nick = nick
        self.oauth_token = oauth_token
        self.channel = channel

        self.connect_message = 'tmi.twitch.tv 376 {} '.format(self.nick)
        self.socket = socket.socket()
        self.readbuffer = ""

        self.socket.connect((self.HOST, self.PORT))

        self.connected = False

        self._thread = Thread(target=self.run)
        self._thread.setDaemon(True)
        self._thread.start()

    def _send_helper(self, message):
        """
        Appends carriagle and new line automatically to messages
        as well as sending it as bytes and converting from `UTF-8`
        """
        message += '\r\n'
        self.socket.send(bytes(message, 'UTF-8'))

    def run(self):
        self._send_helper('PASS oauth:{}'.format(self.oauth_token))
        self._send_helper('NICK {}'.format(self.nick))
        while True:
            self.readbuffer += self.socket.recv(1024).decode('UTF-8')

            temp = self.readbuffer.split('\n')
            self.readbuffer = temp.pop()

            for line in temp:
                line = line.rstrip()
                line = line.split(':', 2)
                
                # Handles PING/PONG of server
                if line[0] == "PING" or line[0] == "PING ":
                    self._send_helper('PONG {}'.format(line[1]))
                    break
                # Handles the connection method and joins the channel once 
                # connected
                elif line[1] == self.connect_message:
                    self.connected = True
                    self._send_helper('JOIN #{}'.format(self.channel))
                    break
                # Rest of the code looks for and handles messages
                server_controls = line[1].split()
                if len(server_controls) > 0 and server_controls[1] == 'PRIVMSG':
                    sender = server_controls[0].split('!', 1)[0]
                    message = line[2]
                    self.chat_signal.emit(sender, message, self.PLATFORM)
                    break
                        
if __name__ == '__main__':
    import time
    irc_bot = ReadOnlyIRCBot('beohoff', nick='beohoff')
    while True:
        time.sleep(1)
