import os
import sys
import asyncio

from .website_plugin import WebsitePlugin
from communication_protocols import JavascriptWebscraper


class Youtube(WebsitePlugin):
    def __init__(self):
        super().__init__('youtube')

    def activate(self, settings):
        url = None
        if 'youtube_url' in settings:
            url = settings['youtube_url']
        elif 'channel_id' in settings:
            url = settings['channel_id']
        webscraper_path = os.path.realpath(os.path.join(os.path.dirname(__file__),
                                                        '..',
                                                        'communication_protocols',
                                                        'javascript_webscraper.py'))

        self.process = asyncio.ensure_future(asyncio.create_subprocess_exec(sys.executable,
                                                                            webscraper_path,
                                                                            url,
                                                                            'all-comments',
                                                                            'yt-user-name',
                                                                            'comment-text'))

        asyncio.ensure_future(self._reoccuring())
