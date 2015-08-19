from PyQt5 import QtWidgets, QtGui, Qt
from gui import MainWindow

class _StandardTextFormat(QtGui.QTextCharFormat):
    """
    Standard text format for `MessageArea`
    """
    def __init__(self):
        super(_StandardTextFormat, self).__init__()
        self.setFontWeight(QtGui.QFont.DemiBold)
        self.setForeground(Qt.blue)
        self.setFontPointSize(13)

class MessageArea(QtWidgets.QTextEdit):
    def __init__(self, parent=None):
        super(MessageArea, self).__init__(parent)
        self.setReadOnly(True)
        
        # styling
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.viewport().setAutoFillBackground(False)

    @QtCore.pyqtSlot(str, str, int)
    def chat_string_slot(self, sender, message, platform):
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
        self._time_signal.emit(formatted_datetime)
        # the platform name and timestamp are in a bracket. Example: `[YT@12:54:00]:`
        bracket_string = ' [{}]: '.format(self.StatusBarSelector(platform).name[0])
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

    def _set_up_text_formats(self):
        """
        Helper method to create the name formater helpers
        `self.name_format` is used for names
        `self.test_formater` is used for the messages
        """
        self.name_formats = []
        for color in (Qt.red, Qt.darkMagenta, Qt.yellow, Qt.green):
            name_format = _StandardTextFormat()
            name_format.set
            self.name_formats.append(name_format)

        #text format is black, normal fontweight, and size 13
        self.text_format = QtGui.QTextCharFormat()
        self.text_format.setFontWeight(self.fontWeight())
        self.text_format.setForeground(Qt.white)
        self.text_format.setFontPointSize(13)
