from . import WebsitePlugin
from communication_protocols import JavascriptWebscraper

class Youtube(WebsitePlugin):
    def __init__(self):
        super(Youtube, self).__init__('youtube')

    def activate(self, settings):
        super(Youtube, self).activate()
        url = None
        if 'youtube_url' in settings:
            url = settings['youtube_url']
        elif 'channel_id' in settings:
            url = settings['channel_id']
        self._javascript_webscraper = JavascriptWebscraper(
                url,
                'all-comments',
                'yt-user-name',
                'comment-text',
                self)
