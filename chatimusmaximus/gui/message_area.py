from datetime import datetime
import queue
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
        # get the timestamp
        formatted_datetime = datetime.now().strftime("%H:%M:%S")
        self.time_signal.emit(formatted_datetime)

        self._insert_and_format(sender, message, platform)
        # get scroll bar and set to maximum
        scroll_bar = self.verticalScrollBar()
        scroll_bar.setValue(scroll_bar.maximum())

    def _insert_and_format(self, sender, message, platform):
        """
        Helper method to handle the text display logic
        """
        # get cursor
        cursor = self.textCursor()
        # set the format to the name format, i.e. Bold and colored
        cursor.setCharFormat(self.name_formats[platform])
        # the platform name is in a bracket. Example: `[Youtube]:`
        bracket_string = ' [{}]: '.format(platform.title())
        # inserts the sender name next to the platform
        cursor.insertText(sender + bracket_string)
        # sets format to text format, i.e. normal and white
        cursor.setCharFormat(self.text_format)
        # inserts message
        cursor.insertText(message)
        # inserts newline
        cursor.insertBlock()
        self.setTextCursor(cursor)
