from PyQt5 import QtWidgets, QtCore, QtGui
import html, json
from datetime import datetime

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        """
        MainWindow uses a QTextEdit to display chat
        """
        # initialize parent class. Req'd for PyQt subclasses
        super(MainWindow, self).__init__(parent)

        # set title window to `CHATIMUSMAXIMUS`
        self.setWindowTitle("CHATIMUSMAXIMUS")

        # create the text edit used to display the text
        self.text_edit = QtWidgets.QTextEdit(parent=self)
        self.text_edit.setReadOnly(True)

        self.setCentralWidget(self.text_edit)

        # sets name and text formats
        self.name_format = None
        self.text_format = None
        self._set_up_text_formats()

    @QtCore.pyqtSlot(str, str, str)
    def chat_string_slot(self, sender, message, platform):
        self._chat_formater(sender, message, platform)

    @QtCore.pyqtSlot(QtCore.QByteArray, str)
    def chat_byte_slot(self, qbyte_array, platform):
        text = str(qbyte_array).split('\\r\\n')[12]
        text = text.split('&', maxsplit=2)

        host = text[0][5:]
        user = html.unescape(text[1][7:])
        message = html.unescape(text[2][8:][:-1])
        self._chat_formater(user, message, platform)
    
    # FIXME: poor method name, not descriptive of what it does
    def _chat_formater(self, sender, message, platform):
        """
        Helper method to handle the text display logic
        """
        # get cursor from text edit
        cursor = self.text_edit.textCursor()

        # set the format to the name format
        cursor.setCharFormat(self.name_format)
        # get the timestamp
        formatted_datetime = datetime.now().strftime("%H:%M:%S")
        # the platform name and timestamp are in a bracket. Example: `[YT@12:54:00]:`
        bracket_string = ' [{}@{}]: '.format(platform, formatted_datetime)
        # inserts the sender name next to the platform & timestamp
        cursor.insertText(sender + bracket_string)
        
        # sets format to text format
        cursor.setCharFormat(self.text_format)
        # inserts message
        cursor.insertText(message)
        # inserts newline
        cursor.insertBlock()

    def _set_up_text_formats(self):
        """
        Helper method to create the name formater helpers
        `self.name_format` is used for names
        `self.test_formater` is used for the messages
        """
        # name format is Demibold, blue, with size 13
        self.name_format = QtGui.QTextCharFormat()
        self.name_format.setFontWeight(QtGui.QFont.DemiBold)
        self.name_format.setForeground(QtCore.Qt.blue)
        self.name_format.setFontPointSize(13)

        #text format is black, normal fontweight, and size 13
        self.text_format = QtGui.QTextCharFormat()
        self.text_format.setFontWeight(self.text_edit.fontWeight())
        self.text_format.setForeground(QtCore.Qt.black)
        self.text_format.setFontPointSize(13)
