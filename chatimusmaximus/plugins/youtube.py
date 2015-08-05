from plugins import IPlugin
from gui import MainWindow
from utils import Messager
from communication_protocols import JavascriptWebscraper

class YoutubePlugin(IPlugin):
    def __init__(self, settings):
        # use the trivial instance `_messager` to get around multiple inheritance
        # problems with PyQt
        self._messager = Messager(MainWindow.StatusBarSelector.Youtube)
        # Duck type the `chat_signal` onto the `Socket` instance/class
        self.chat_signal = self._messager.chat_signal

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
                self._messager.recieve_chat_data)
