import asyncio

from .website_plugin import WebsitePlugin
from communication_protocols import PATHS
from util import get_current_youtube_link


class Youtube(WebsitePlugin):
    def __init__(self):
        super().__init__('youtube')

    def activate(self, settings):
        url = None
        if 'client_secrets_file' in settings:
            url = get_current_youtube_link(settings['client_secrets_file'])
        elif 'youtube_url' in settings:
            url = settings['youtube_url']
        elif 'channel_id' in settings:
            url = settings['channel_id']

        asyncio.ensure_future(self.start_subprocess(PATHS['javascript_path'],
                                                    url,
                                                    'all-comments',
                                                    'yt-user-name',
                                                    'comment-text'))
