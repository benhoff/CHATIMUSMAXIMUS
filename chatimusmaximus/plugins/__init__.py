import os
import imp
from PyQt5 import QtCore

class IPluginRegistry(type):
    plugins = []
    def __init__(cls, name, bases, attrs):
        if name != 'IPlugin':
            IPluginRegistry.plugins.append(cls)

class _PyQtCompat(QtCore.QObject):
    """
    Can't subclass from multiple classes with PyQt
    """
    chat_signal = QtCore.pyqtSignal(str, str, str)
    connected_signal = QtCore.pyqtSignal(bool, str)

    def __init__(self, parent=None):
        super(_PyQtCompat, self).__init__(parent)

class IPlugin(object, metaclass=IPluginRegistry):
    def __init__(self, platform):
        super(IPlugin, self).__init__()
        self.platform = platform

        self._pyqt_compat = _PyQtCompat()
        self.chat_signal = self._pyqt_compat.chat_signal
        self.connected_signal = self._pyqt_compat.connected_signal

    def message_function(self, sender, message):
        self.chat_signal.emit(sender, message, self.platform)

    def connected_function(self, bool):
        self.connected_signal.emit(bool, self.platform)

def get_plugins():
    directory = os.path.dirname(os.path.realpath(__file__))
    for filename in os.listdir(directory):
        # TODO: Figure out cleaner way to do this
        filename = os.path.join(directory, filename)
        modname, ext  = os.path.splitext(filename)
        if ext == '.py' and modname != 'base_plugin' and modname != '__init__':
            file_, path, descr = imp.find_module(modname, [dir])
            if file_:
                mod = imp.load_module(modname, file_, path, descr)
