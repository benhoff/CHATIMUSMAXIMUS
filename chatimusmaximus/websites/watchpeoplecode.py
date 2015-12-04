import asyncio

from .website_plugin import WebsitePlugin
from communication_protocols import PATHS


class WatchPeopleCode(WebsitePlugin):
    def __init__(self):
        super().__init__(platform='watchpeoplecode')

    def activate(self, settings, **kwargs):
        streamer_name = settings['channel']
        namespace = '/chat'
        name = 'http://www.watchpeoplecode.com/socket.io/1/'

        asyncio.ensure_future(self.start_subprocess(PATHS['socket_path'],
                                                    streamer_name,
                                                    namespace,
                                                    name))
