import websocket
import json
import requests
from threading import Thread, Event
import html
from PyQt5 import QtCore

class ServerPinger(Thread):
    """
    Socket.io server requires feedback from the client to let it know that 
    the client is still 'alive'. This class does that without blocking
    """
    # this makes so the program exits if only this thread type is left
    # equals good
    daemon = True

    def __init__(self, ping_interval, ping_function, *args, **kwargs):
        self.ping_interval = ping_interval
        self.ping_function = ping_function
        super(ServerPinger, self).__init__(*args, **kwargs)
        self.event_instance = Event()

    def run(self):
        self.event_instance.wait(self.ping_interval)
        while not self.event_instance.is_set():
            self.ping_function()
            self.event_instance.wait(self.ping_interval)

    def cancel(self):
        self.event_instance.set()

class Messager(QtCore.QObject):
    """
    Super trivial class to get around the issue with multiple inhertiance in
    PyQt
    """
    chat_signal = QtCore.pyqtSignal(str, str)
    def __init__(self, parent=None):
        super(Messager, self).__init__(parent)

    def recieve_chat_data(self, sender, message):
        self.chat_signal.emit(sender, message)

class SocketThread(Thread):
    # If only dameon threads are left, exit the program
    dameon = True
    def __init__(self, streamer_name, namespace='/chat', *args, **kwargs):
        self.socket = Socket(streamer_name, namespace)
        self.chat_signal = self.socket.chat_signal
        super(SocketThread, self).__init__(*args, **kwargs)

    def run(self):
        self.socket.run_forever()


class Socket(websocket.WebSocketApp):
    def __init__(self, streamer_name, namespace='/chat'):
        self._streamer_name = streamer_name
        self.namespace = namespace 
        website_url = 'http://www.watchpeoplecode.com/socket.io/1/'
        r = requests.post(website_url)
        params = r.text

        # unused variables are connection_timeout and supported_formats
        key, heartbeat_timeout, _, _ = params.split(':') 
        
        # alters URL to be more websocket...ie
        website_socket = website_url.replace('http', 'ws') + 'websocket/'
        super(Socket, self).__init__(website_socket + key,
                                     on_open=self.on_open, on_close=self.on_close,
                                     on_message=self.on_message, 
                                     on_error=self.on_error)
        
        # create a pinger to re-ping the server so we don't timeout
        self._server_pinger = ServerPinger(int(heartbeat_timeout) - 2,
                                           self._ping_server)

        # start the server pinger
        self._server_pinger.start()

        # use the trivial instance `_messager` to get around multiple inheritance
        # problems with PyQt
        self._messager = Messager()
        # Duck type the `chat_signal` onto the `Socket` instance/class
        self.chat_signal = self._messager.chat_signal

    def on_open(self, *args):
        print('Websocket open!')

    def on_close(self, *args):
        print('Websocket closed!')

    def _ping_server(self):
        # this pings the server
        self.send_packet_helper(2)
    
    def on_message(self, *args):
        message = args[1].split(':', 3)
        key = int(message[0])
        namespace = message[2]

        if len(message) >= 4:
           data = message[3]
        else:
            data = ''
        if key == 1 and args[1] == '1::':
            self.send_packet_helper(1)
        elif key == 1 and args[1] == '1::{}'.format(self.namespace):
            self.send_packet_helper(5, data={'name':'initialize'})
            data = {'name':'join', 'args':['{}'.format(self._streamer_name)]}
            self.send_packet_helper(5, data=data)
        elif key  == 5:
            data = json.loads(data, )
            if data['name'] == 'message':
                message = data['args'][0]
                sender = html.unescape(message['sender'])
                message = html.unescape(message['text'])
                self._messager.recieve_chat_data(sender, message)

    def on_error(self, *args):
        print(args[1])

    def disconnect(self):
        callback = ''
        data = ''
        # '1::namespace'
        self.send(':'.join([str(self.TYPE_KEYS['DISCONNECT']), 
                           callback, self.namespace, data]))

    def send_packet_helper(self, 
                           type_key, 
                           data=None):

        if data is None:
            data = ''
        else:
            data = json.dumps(data)
        
        # NOTE: callbacks currently not implemented
        callback = ''
        message = ':'.join([str(type_key), callback, self.namespace, data])
        self.send(message)
    
if __name__ == '__main__':
    streamer_name = 'beohoff'
    # this is default for the flask app
    socket = Socket(streamer_name)
    socket.run_forever()
