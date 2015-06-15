from PyQt5 import QtCore
class Messager(QtCore.QObject):
    """
    Super trivial class to get around the issue with multiple inhertiance in
    PyQt
    """
    chat_signal = QtCore.pyqtSignal(str, str)
    def __init__(self, parent=None):
        super(Messager, self).__init__(parent)

    def recieve_chat_data(self, sender, message):
        self.chat_signal.emit(sender, message)
