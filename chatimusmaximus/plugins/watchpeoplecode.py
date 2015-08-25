from plugins import IPlugin
from communication_protocols import ReadOnlyWebSocket

class WatchPeopleCodePlugin(IPlugin):
    def __init__(self, settings): 
        super(WatchPeopleCodePlugin, self).__init__(platform='watchpeoplecode')
        streamer_name = settings['channel']
        self._websocket = ReadOnlyWebSocket(streamer_name,
                                            '/chat',
                                            'http://www.watchpeoplecode.com/socket.io/1/',
                                            self)
