from plugins import IPlugin
from utils import Messager
from communication_protocols import JavascriptWebscraper

class YoutubePlugin(IPlugin):
    def __init__(self, settings):
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
                self.recieve_chat_data)
