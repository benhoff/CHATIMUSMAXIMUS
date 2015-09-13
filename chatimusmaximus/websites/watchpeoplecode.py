from . import WebsitePlugin
from communication_protocols import ReadOnlyWebSocket

class WatchPeopleCode(WebsitePlugin):
    def __init__(self): 
        super(WatchPeopleCode, self).__init__(platform='watchpeoplecode')

    def activate(self, settings):
        super(WatchPeopleCode, self).activate()
        streamer_name = settings['channel']
        self._websocket = ReadOnlyWebSocket(streamer_name,
                                            '/chat',
                                            'http://www.watchpeoplecode.com/socket.io/1/',
                                            self)
