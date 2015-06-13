import websocket
import json
import requests


class Socket(websocket.WebSocketApp):
    def __init__(self, namespace='/chat'):
        self.namespace = namespace 
        #port_number =  5000
        website_url = 'http://www.watchpeoplecode.com/socket.io/1/'
        r = requests.post(website_url)
        params = r.text
        key, heartbeat_timeout, connection_timeout, supported_transports = \
                params.split(':') 

        website_socket = website_url.replace('http', 'ws') + 'websocket/'
        super(Socket, self).__init__(website_socket + key,
                                     on_open=self.on_open, on_close=self.on_close,
                                     on_message=self.on_message, 
                                     on_error=self.on_error)

    def on_open(self, *args):
        print('Websocket open!')

    def on_close(self, *args):
        print('Websocket closed!')
    
    def on_message(self, *args):
        message = args[1].split(':', 3)
        key = int(message[0])
        callback =message[1]
        namespace = message[2]

        if len(message) >= 4:
           data = message[3]
        else:
            data = ''
        if key == 1 and args[1] == '1::':
            self.send_packet_helper(1)
        elif key == 1 and args[1] == '1::{}'.format(self.namespace):
            self.send_packet_helper(5, data={'name':'initialize'})
            self.send_packet_helper(5, data={'name':'join', 'args':['beohoff']})
        if key == 2:
            pass
        if key  == 5:
            data = json.loads(data)
            if data['name'] == 'message':
                message = data['args'][0]
                self.message_signal(message['sender'], message['text'])


    def message_signal(self, sender, message):
        # TODO: make this so much better
        print(sender, message)

    def on_error(self, *args):
        print(args[1])

    def disconnect(self):
        callback = ''
        data = ''
        # '1::namespace'
        self.send(':'.join([str(self.TYPE_KEYS['DISCONNECT']), 
                           callback, self.namespace, data]))
    """    
    def emit(self, type_key, data):
        data = json.dumps(data)
        self.send(':'
    """
    def send_packet_helper(self, 
                           type_key, 
                           data=None, 
                           callback=None):

        if callback is not None:
            print('Callbacks not implemented in `send_packet_helper` in `Socket`')
        if data is None:
            data = ''
        else:
            data = json.dumps(data)

        callback = ''
        message = ':'.join([str(type_key), callback, self.namespace, data])
        self.send(message)
    
    LISTNER_KEYS = {'DISCONNECT':0,
                    'CONNECT':1,
                    'HEARTBEAT':2,
                    'MESSAGE':3,
                    'JSON':4,
                    'EVENT':5,
                    'ACK':6,
                    'ERROR':7}

    # for reference!
    TYPE_KEYS = {'CONNECT':0, 
                 'DISCONNECT':1, 
                 'EVENT':2, 
                 'ACK':3, 
                 'ERROR':4,
                 'BINARY_EVENT':5,
                 'BINARY_ACK':6}

if __name__ == '__main__':
    # TODO: need to build in like pinger so that we stay connected to the server
    # TODO: need to parse our data

    streamer_name = 'beohoff'
    # this is default for the flask app
    socket = Socket()
    socket.run_forever()
