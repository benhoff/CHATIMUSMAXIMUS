import os
import sys
import asyncio
import subprocess

from .website_plugin import WebsitePlugin
from communication_protocols import ReadOnlyXMPPBot


class Livecoding(WebsitePlugin):
    # FIXME: migrate to asyncio library
    def __init__(self):
        super().__init__('livecoding')
        self._xmpp_echo = None

    def activate(self, settings):
        settings_nick = settings['bot_nick']
        bot_nick = settings_nick if settings_nick != str() else 'EchoBot'
        password = settings['password']
        local = settings['name']
        domain = 'livecoding.tv'
        resource = 'CHATIMUSMAXIMUS'
        room = settings['room']
        if not room:
            room = '{}@chat.livecoding.tv'.format(jid.name)
        path = os.path

        xmpp_bot_path = path.realpath((os.path.join(os.path.dirname(__file__),
                                          '..',
                                          'communication_protocols',
                                          'xmpp_client.py')))

        self.process = asyncio.ensure_future(asyncio.create_subprocess_exec(sys.executable,
                                                                            xmpp_bot_path,
                                                                            local,
                                                                            domain,
                                                                            room,
                                                                            resource,
                                                                            password,
                                                                            stderr=sys.stderr))

        asyncio.ensure_future(self._reoccuring())
