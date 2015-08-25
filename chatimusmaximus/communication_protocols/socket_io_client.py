import json
import requests
import html
import logging
import asyncio
import websocket

# TODO: switch to using the WebSocket and the asyncio lib
class ReadOnlyWebSocket(websocket.WebSocketApp):
    # NOTE: chat_signal defined in `__init__`

    def __init__(self, 
                 streamer_name, 
                 namespace, 
                 website_url,
                 plugin=None):

        self._streamer_name = streamer_name
        self.namespace = namespace 
        self._website_url = website_url 
        self.key, heartbeat = self._connect_to_server_helper()
        self.plugin = plugin

        
        # alters URL to be more websocket...ie
        self._website_socket = self._website_url.replace('http', 'ws') + 'websocket/'
        super(ReadOnlyWebSocket, self).__init__(
                self._website_socket + self.key,
                on_open=self.on_open, on_close=self.on_close,
                on_message=self.on_message, 
                on_error=self.on_error)
        asyncio.get_event_loop().run_in_executor(None, self.repeat_run_forever)

    def repeat_run_forever(self):
        while True:
            try:
                self.run_forever()
            except:
                if self.plugin is not None:
                    self.plugin.connected_function(False)
                key, _ = self._connect_to_server_helper()
                self.url = self._website_socket + key

    def _connect_to_server_helper(self):
        r = requests.post(self._website_url)
        params = r.text

        # unused variables are connection_timeout and supported_formats
        key, heartbeat_timeout, _, _ = params.split(':') 
        heartbeat_timeout = int(heartbeat_timeout)
        return key, heartbeat_timeout

    def on_open(self, *args):
        logging.info('Websocket open!')

    def on_close(self, *args):
        logging.info('Websocket closed :(')

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
            if self.plugin is not None:
                self.plugin.connected_function(True)
        elif key == 2:
            self.send_packet_helper(2)
        elif key  == 5:
            data = json.loads(data, )
            if data['name'] == 'message':
                message = data['args'][0]
                sender = html.unescape(message['sender'])
                message = html.unescape(message['text'])
                if self.plugin is not None:
                    self.plugin.message_function(sender, message)

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
