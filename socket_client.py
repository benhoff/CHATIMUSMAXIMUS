import websocket
import requests

def on_open(web_socket):
    print('Websocket open!')

def on_message(web_socket, message):
    print(message)

def on_error(web_socket, e):
    print(e)

def on_close(web_socket):
    print('Websocket closed!')

if __name__ == '__main__':
    streamer_name = 'beohoff'
    # this is default for the flask app
    port_number =  5000
    """
    website_socket= 'ws://www.watchpeoplecode.com/streamer/{}:{}/chat'.format(
            streamer_name, port_number)
    """
    params = {'EIO':3, 'transport':'websocket'}
    website_url = 'http://www.watchpeoplecode.com/socket.io/1/'
    r = requests.post(website_url)
    params = r.text
    key, heartbeat_timeout, connection_timeout, supported_transports = \
            params.split(':') 

    website_socket = 'ws://www.watchpeoplecode.com/socket.io/1/websocket/'
    web_socket = websocket.WebSocketApp(website_socket + key)
    web_socket.on_open = on_open
    web_socket.on_error = on_error
    web_socket.on_message = on_message
    web_socket.on_close = on_close
    web_socket.run_forever()
