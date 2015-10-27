from .website_plugin import WebsitePlugin
import communication_protocols


class Twitch(WebsitePlugin):
    def __init__(self):
        """
        This class is a convince/internal api wrapper around another plugin
        """
        super(Twitch, self).__init__(platform='twitch')

    def activate(self, settings):
        super(Twitch, self).activate()
        create_bot = communication_protocols.create_irc_bot
        irc_client = create_bot(settings['nick'],
                                settings['oauth_token'],
                                'irc.twitch.tv',
                                channel=settings['channel'],
                                plugin=self)

        irc_client.create_connection()
        irc_client.add_signal_handlers()
