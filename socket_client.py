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

        #self.send_packet_helper(0)
        #self.send_packet_helper(5, data="{'name':'initialize'}")

    def on_open(self, *args):
        print('Websocket open!')

    def on_close(self, *args):
        print('Websocket closed!')
    
    def on_message(self, *args):
        message = args[1].split(':')
        key = int(message[0])
        callback =message[1]
        namespace = message[2]

        if len(message) == 4:
           data = message[3]
        else:
            data = ''
        print('Key: ', key) 
        if key == 1 and args[1] == '1::':
            print("Connecting to namespace!")
            self.send_packet_helper(1)
        elif key == 1 and args[1] == '1::/chat':
            self.send_packet_helper(5, data={'name':'initialize'})
            self.send_packet_helper(5, data={'name':'join', 'args':['beohoff']})
        if key == 2:
            pass

        print(args[1])
        

    def on_error(self, *args):
        print(args)

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
        print("Packet helper: ", message)
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
    streamer_name = 'beohoff'
    # this is default for the flask app
    socket = Socket()
    socket.run_forever()
