import websocket
import requests
import threading
import time

def onopen(ws):
    def run(*args):
        for i in range(3):
            time.sleep(1)
            ws.send('Hello {}'.format(i))
    threading.start_new_thread(run,())
    print('Websocket open!')

def onmessage(message):
    print('Message: {}'.format(message))

def on_error(ws, e):
    print(e)

if __name__ == '__main__':
    streamer_name = 'beohoff'
    # this is default for the flask app
    port_number =  5000
    website_socket= 'ws://www.watchpeoplecode.com/streamer/{}:{}/chat'.format(
            streamer_name, port_number)
    website_url = 'http://www.watchpeoplecode.com/streamer/beohoff:{}/chat/'.format(port_number)
    #header = {'username':'beohoff'}
    r = requests.post(website_url)
    print(r.text, r)
    ws = websocket.WebSocketApp(website_socket+ '/chat',
            on_message = onmessage)
    ws.on_open = onopen
    ws.on_error = on_error
    ws.run_forever()
