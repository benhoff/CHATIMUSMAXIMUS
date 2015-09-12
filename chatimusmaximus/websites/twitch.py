from plugins.websites import IPlugin
import communication_protocols

class TwitchPlugin(IPlugin):
    def __init__(self, settings):
        """
        This class is a convince/internal api wrapper around another plugin
        """
        super(TwitchPlugin, self).__init__(platform='twitch')
        self._settings = settings

    def activate(self):
        super(TwitchPlugin, self).activate()
        irc_client = communication_protocols.create_irc_bot(
                self._settings['nick'],                                     
                self._settings['oauth_token'],
                'irc.twitch.tv',
                channel=self._settings['channel'],
                plugin=self)

        irc_client.create_connection()
        irc_client.add_signal_handlers()
