from plugins import IPlugin
from communication_protocols import JavascriptWebscraper

class YoutubePlugin(IPlugin):
    def __init__(self, settings):
        super(YoutubePlugin, self).__init__('youtube')
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
