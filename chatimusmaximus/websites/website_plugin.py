import os
import re
import sys
import signal
import asyncio
import locale

from parse import parse
from PyQt5 import QtCore
from pluginmanager import IPlugin


class WebsitePlugin(QtCore.QObject):
    chat_signal = QtCore.pyqtSignal(str, str, str)
    connected_signal = QtCore.pyqtSignal(bool, str)

    def __init__(self, platform, parent=None):
        super().__init__(parent)
        self.platform = platform
        # TODO: change from `process` to `subprocess`
        self.process = None
    
    async def start_subprocess(self, path_script, *args, **kwargs):
        self.process = await asyncio.create_subprocess_exec(
            sys.executable,
            '-u',
            path_script,
            *args,
            stdout=asyncio.subprocess.PIPE,
            preexec_fn=os.setsid,
            **kwargs)
        print('subprocess {} started'.format(self.platform))
        await self._reoccuring()

    async def _reoccuring(self):
        while True:
            async for line in self.process.stdout:
                self._parse_communication(line.decode(locale.getpreferredencoding(False)))

    def _parse_communication(self, comms):
        try:
            command, body = comms.split(sep=' ', maxsplit=1)
            body = body.rstrip()
        except ValueError:
            command = comms.rstrip()

        if command == 'MSG':
            nick, message = parse('NICK: {} BODY: {}', body)
            self.chat_signal.emit(nick, message, self.platform)
        elif command == 'CONNECTED':
            self.connected_signal.emit(True, self.platform)
        elif command == 'DISCONNECTED':
            self.connected_signal.emit(False, self.platform)


# NOTE: Forcing `WebsitePlugin` to be subclass of IPlugin
# for ease of parsing
IPlugin.register(WebsitePlugin)


