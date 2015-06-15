import socket
import string
import os
from threading import Thread
from messager import Messager

class ReadOnlyIRCBot(object):
    HOST = 'irc.twitch.tv'
    PORT = 6667
    
    def __init__(self, channel, nick=None, oauth_token=None):
        self.channel = channel
        self.readbuffer = ""
        if nick is None:
            nick = channel 
        if oauth_token is None:
            oauth_token = os.getenv('TWITCH_KEY')
        self.oauth_token = oauth_token
        self.nick = nick

        self.socket = socket.socket()
        self.socket.connect((self.HOST, self.PORT))

        self.connected = False
        self._messager = Messager()
        self.chat_signal = self._messager.chat_signal

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
            self.readbuffer = self.readbuffer + \
                    self.socket.recv(1024).decode('UTF-8')

            temp = str.split(self.readbuffer, '\n')
            self.readbuffer = temp.pop()
            print('length of temp: ', len(temp))

            for line in temp:
                line = line.rstrip()
                # TODO: switch back to using just `split()`
                line = line.split(':', 2)

                if line[0] == "PING":
                    print('ping!')
                    self.socket.send(bytes("PONG {}".format(line[1]), 
                                           "UTF-8"))
                    break
                # TODO: Just parse `PRIVMSG` 
                # NOTE: If use `split()` this has extra space on the end!!!
                elif line[1] == 'tmi.twitch.tv 376 {} '.format(self.nick):
                    self.connected = True
                    self._send_helper('JOIN #{}'.format(self.channel))
                    break
                test_line = line[1].split()
                if len(test_line) > 0:
                    if test_line[1] == 'PRIVMSG':
                        if len(line) > 1:
                            message = line[2]
                        else:
                            message = 'PLACEHOLDER'
                        self._messager.recieve_chat_data(test_line[0], message)
                for index, i in enumerate(line):
                    print(line[index])

if __name__ == '__main__':
    irc_bot = ReadOnlyIRCBot('beohoff')


