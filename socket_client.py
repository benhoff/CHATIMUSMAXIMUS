import websocket
import requests
import threading
import time

def onopen(ws):
    print('Websocket open!')

def onmessage(ws, message):
    print(message)

def on_error(ws, e):
    print(e)

if __name__ == '__main__':
    streamer_name = 'beohoff'
    # this is default for the flask app
    port_number =  5000
    """
    website_socket= 'ws://www.watchpeoplecode.com/streamer/{}:{}/chat'.format(
            streamer_name, port_number)
    """
    params = {'EIO':3, 'transport':'websocket'}
    website_socket = 'ws://www.watchpeoplecode.com/streamer/beohoff:5000'
    website_url = 'http://www.watchpeoplecode.com/socket.io/1/'
    test_website_socket = 'ws://www.watchpeoplecode.com/socket.io/1/websocket/'
    #header = {'username':'beohoff'}
    r = requests.post(website_url)
    key = r.text.split(':')[0]
    """
    ws = websocket.WebSocketApp(website_socket+ '/chat/'+key,
            on_message = onmessage)
    """
    ws = websocket.WebSocketApp(test_website_socket + key,
            on_message = onmessage)
            #subprotocols=["chat"])
    ws.on_open = onopen
    ws.on_error = on_error
    ws.run_forever()
