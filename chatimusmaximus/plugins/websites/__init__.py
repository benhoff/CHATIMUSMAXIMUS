import os
import imp
from PyQt5 import QtCore
from yapsy.IPlugin import IPlugin
from yapsy.PluginManager import 

class _PyQtCompat(QtCore.QObject):
    """
    Can't subclass from multiple classes with PyQt
    """
    chat_signal = QtCore.pyqtSignal(str, str, str)
    connected_signal = QtCore.pyqtSignal(bool, str)

    def __init__(self, parent=None):
        super(_PyQtCompat, self).__init__(parent)

class WebsitePlugin(IPlugin):
    def __init__(self, platform):
        super(WebsitePlugin, self).__init__()
        self.platform = platform

        self._pyqt_compat = _PyQtCompat()
        self.chat_signal = self._pyqt_compat.chat_signal
        self.connected_signal = self._pyqt_compat.connected_signal

    def message_function(self, sender, message):
        self.chat_signal.emit(sender, message, self.platform)

    def connected_function(self, bool):
        self.connected_signal.emit(bool, self.platform)
