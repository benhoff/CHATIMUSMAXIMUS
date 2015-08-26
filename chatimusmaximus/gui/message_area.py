from datetime import datetime
import threading
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import Qt

class _StandardTextFormat(QtGui.QTextCharFormat):
    """
    Standard text format for `MessageArea`
    """
    def __init__(self, text_color=Qt.white, font=QtGui.QFont.DemiBold):
        super(_StandardTextFormat, self).__init__()
        self.setFontWeight(font)
        self.setForeground(text_color)
        self.setFontPointSize(13)

class MessageArea(QtWidgets.QTextEdit):
    time_signal = QtCore.pyqtSignal(str)
    def __init__(self, parent=None):
        self._lock = threading.Lock()
        super(MessageArea, self).__init__(parent)
        self.setReadOnly(True)
        self.text_format = _StandardTextFormat(font=self.fontWeight())
        
        # styling
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.viewport().setAutoFillBackground(False)

        self.name_formats = {} 

    def set_color(self, color, platform):
        if platform in self.name_formats:
            format = self.name_formats[platform]
            format.setForeground(QtGui.QColor(color))
        else:
            self.name_formats[platform] = _StandardTextFormat(QtGui.QColor(color))
    
    @QtCore.pyqtSlot(str, str, str)
    def chat_slot(self, sender, message, platform):
        with self._lock:
            self._chat_formater(sender, message, platform)

        # get scroll bar and set to maximum
        scroll_bar = self.verticalScrollBar()
        scroll_bar.setValue(scroll_bar.maximum())

    # FIXME: poor method name, not descriptive of what it does
    def _chat_formater(self, sender, message, platform):
        """
        Helper method to handle the text display logic
        """
        # get cursor
        cursor = self.textCursor()

        # set the format to the name format
        cursor.setCharFormat(self.name_formats[platform])
        # get the timestamp
        formatted_datetime = datetime.now().strftime("%H:%M:%S")
        self.time_signal.emit(formatted_datetime)
        # the platform name and timestamp are in a bracket. Example: `[YT@12:54:00]:`
        bracket_string = ' [{}]: '.format(platform.title())
        # inserts the sender name next to the platform & timestamp
        cursor.insertText(sender + bracket_string)
        
        # sets format to text format
        cursor.setCharFormat(self.text_format)
        # inserts message
        cursor.insertText(message)
        # inserts newline
        cursor.insertBlock()
        cursor.movePosition(QtGui.QTextCursor.End, QtGui.QTextCursor.MoveAnchor)
        self.setTextCursor(cursor)
