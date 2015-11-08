import os
import sys
import asyncio

from .website_plugin import WebsitePlugin
from communication_protocols import ReadOnlyWebSocket


class WatchPeopleCode(WebsitePlugin):
    def __init__(self):
        super().__init__(platform='watchpeoplecode')

    def activate(self, settings):
        streamer_name = settings['channel']
        namespace = '/chat'
        name = 'http://www.watchpeoplecode.com/socket.io/1/'
        socket_client_path = os.path.realpath(os.path.join(os.path.dirname(__file__),
                                                           '..',
                                                           'communication_protocols',
                                                           'socket_io_client.py'))

        self.start_subprocess(socket_client_path, streamer_name, namespace, name)
