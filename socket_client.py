import websocket
import urllib.request 
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

    website_socket= 'ws://www.watchpeoplecode.com/streamer/{}'.format(
            streamer_name)
    website_url = 'http://www.watchpeoplecode.com/streamer/beohoff'
    request = urllib.request.urlopen(website_url, '/chat') 
    encoding = request.headers.get_content_charset()
    if encoding is None:
        encoding = 'utf-8'
    key = request.read().decode(encoding)
    print(key)
    connection = httplib.HTTPConnection(website_url)
    conn.request('POST', '/chat')
    response = conn.getresponse()
    key = response.read().split(':')[0]
    ws = websocket.WebSocketApp(website_socket+ '/chat',
            on_message = onmessage)
    ws.on_open = onopen
    ws.on_error = on_error
    ws.run_forever()
