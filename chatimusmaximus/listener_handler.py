import asyncio
from PyQt5 import QtCore

class ListenerHandler(QtCore.QObject):
    listeners_signal = QtCore.pyqtSignal(str, str)
    def __init__(self, parent=None):
        super().__init__(parent)
        self.listeners = []
        self.queue = asyncio.Queue()
    
    @asyncio.coroutine
    def handle_messages(self):
        while True:
            sender, message, platform = yield from self.queue.get()
            if listeners:
                # TODO: handle stuff
                pass

    
    @QtCore.pyqtSlot(str, str)
    def listener_slot(self, sender, message, platform=None):
        self.queue.put((sender, message, platform))

