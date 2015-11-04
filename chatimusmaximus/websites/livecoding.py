import os
import sys
import asyncio
import subprocess
import sleekxmpp

from .website_plugin import WebsitePlugin
from communication_protocols import ReadOnlyXMPPBot


class Livecoding(WebsitePlugin):
    # FIXME: migrate to asyncio library
    def __init__(self):
        super().__init__('livecoding')
        self._xmpp_echo = None
        print('made it to init!')
        self.process = asyncio.Future()

    @asyncio.coroutine
    def _reoccuring(self):
        while True:
            if self.process is not None:
                asyncio.sleep(5)
            else:
                print(self.process.communicate())
                yield from asyncio.sleep(1)

    def activate(self, settings):
        print('made it to activate!!!!')
        settings_nick = settings['bot_nick']
        bot_nick = settings_nick if settings_nick != str() else 'EchoBot'
        password = settings['password']
        local = settings['name']
        domain = 'livecoding.tv'
        resource = 'CHATIMUSMAXIMUS'
        """
        jid = sleekxmpp.JID(local=settings['name'],
                            domain='livecoding.tv',
                            resource='CHATIMUSMAXIMUS')
        """

        room = settings['room']
        if room == str():
            room = '{}@chat.livecoding.tv'.format(jid.name)
        print('made it here')

        xmpp_bot_path = os.path.realpath((os.path.join(__file__,
                                          '..',
                                          'communication_protocols',
                                          'xmpp_client.py')))

        print(os.path.isfile(xmpp_bot_path))

        self.process = asyncio.create_subprocess_exec(sys.executable,
                                                      xmpp_bot_path,
                                                      local,
                                                      domain,
                                                      room,
                                                      resource,
                                                      password,
                                                      stderr=sys.stderr)

        yield from self._reoccuring()
        # asyncio.ensure_future(self._reoccuring())
