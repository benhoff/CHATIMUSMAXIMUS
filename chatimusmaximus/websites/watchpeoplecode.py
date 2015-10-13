from . import WebsitePlugin
from communication_protocols import ReadOnlyWebSocket


class WatchPeopleCode(WebsitePlugin):
    def __init__(self):
        super(WatchPeopleCode, self).__init__(platform='watchpeoplecode')

    def activate(self, settings):
        super(WatchPeopleCode, self).activate()
        streamer_name = settings['channel']
        name = 'http://www.watchpeoplecode.com/socket.io/1/'
        self._websocket = ReadOnlyWebSocket(streamer_name,
                                            '/chat',
                                            name,
                                            self)
