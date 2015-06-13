import websocket
import requests

class Socket(websocket.WebSocketApp):
    def __init__(self, namespace=None):
        self.namespace = namespace 
        #port_number =  5000
        website_url = 'http://www.watchpeoplecode.com/socket.io/1/'
        r = requests.post(website_url)
        params = r.text
        key, heartbeat_timeout, connection_timeout, supported_transports = \
                params.split(':') 

        website_socket = website_url.replace('http', 'ws') + 'websocket/'
        super(Socket, self).__init__(website_socket + key)

    def on_open(self):
        print('Websocket open!')

    def on_close(self):
        print('Websocket closed!')

    def on_message(self, message):
        print(message)

    def on_error(self, e):
        print(e)

    def _namespace_helper(self, namespace=None):
        """
        This is a small helper to determine the namespace state.
        """
        if namespace is None and self.namespace is None:
            namespace = ''
        else namespace is None:
            namespace = self.namespace
        return namespace
    
    def disconnect(self, namespace=None):
        namespace = self._namespace_helper(namespace)
        # '0::namespace'
        self.send(':'.join(0, '', namespace, ''))

    def send_packet_helper(self, 
                           type_key, 
                           namespace=None, 
                           data=None, 
                           callback=None):

        if callback is not None:
            print('Callbacks not implemented in `send_packet_helper` in `Socket`')

        callback = ''
        namespace = self._namespace_helper(namespace)
        self.send(':'.join([type_key, callback, namespace, data]))

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
