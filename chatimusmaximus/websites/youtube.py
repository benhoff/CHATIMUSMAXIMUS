import asyncio

from .website_plugin import WebsitePlugin
from communication_protocols import PATHS


class Youtube(WebsitePlugin):
    def __init__(self):
        super().__init__('youtube')

    def activate(self, settings):
        url = None
        if 'youtube_url' in settings:
            url = settings['youtube_url']
        elif 'channel_id' in settings:
            url = settings['channel_id']

        asyncio.ensure_future(self.start_subprocess(PATHS['javascript_path'],
                                                    url,
                                                    'all-comments',
                                                    'yt-user-name',
                                                    'comment-text'))
