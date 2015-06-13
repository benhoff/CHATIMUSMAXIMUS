import websocket
import requests

class Socket(websocket.WebSocketApp):
    def __init__(self):
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

    def on_message(self, message):
        print(message)

    def on_error(self, e):
        print(e)

    def on_close(self):
        print('Websocket closed!')

    def send_packet

if __name__ == '__main__':
    streamer_name = 'beohoff'
    # this is default for the flask app
    socket = Socket()
    socket.run_forever()
