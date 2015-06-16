import websocket
import json
import requests
from threading import Thread, Event
import html
from messager import Messager

class Socket(websocket.WebSocketApp):
    PLATFORM = 'WPC'

    def __init__(self, streamer_name, namespace='/chat'):
        self._streamer_name = streamer_name
        self.namespace = namespace 
        self._website_url = 'http://www.watchpeoplecode.com/socket.io/1/'
        key, heartbeat = self._connect_to_server_helper()
        self._heartbeat = heartbeat/2 
        
        # alters URL to be more websocket...ie
        self._website_socket = self._website_url.replace('http', 'ws') + 'websocket/'
        super(Socket, self).__init__(self._website_socket + key,
                                     on_open=self.on_open, on_close=self.on_close,
                                     on_message=self.on_message, 
                                     on_error=self.on_error)
        
        # start a thread and set the socket to run forever
        self._thread = Thread(target=self.run_forever)
        self._thread.setDaemon(True)
        self._thread.start()

        # use the trivial instance `_messager` to get around multiple inheritance
        # problems with PyQt
        self._messager = Messager()
        # Duck type the `chat_signal` onto the `Socket` instance/class
        self.chat_signal = self._messager.chat_signal

    def _reconnect_to_server(self):
        self._thread.join()
        thread = Thread()
        pass

    def _connect_to_server_helper(self):
        r = requests.post(self._website_url)
        params = r.text

        # unused variables are connection_timeout and supported_formats
        key, heartbeat_timeout, _, _ = params.split(':') 
        heartbeat_timeout = int(heartbeat_timeout)
        return key, heartbeat_timeout

    def on_open(self, *args):
        print('Websocket open!')

    def on_close(self, *args):
        print('Websocket closed!')
        self._thread.join()

    def on_message(self, *args):
        message = args[1].split(':', 3)
        print(message)
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
        elif key == 2:
            self.send_packet_helper(2)
        elif key  == 5:
            data = json.loads(data, )
            if data['name'] == 'message':
                message = data['args'][0]
                sender = html.unescape(message['sender'])
                message = html.unescape(message['text'])
                self._messager.recieve_chat_data(sender, message, self.PLATFORM)

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
