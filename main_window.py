from PyQt5 import QtWidgets, QtCore, QtGui
import html, json

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setWindowTitle("CHATIMUSMAXIMUS")
        self.text_edit = QtWidgets.QTextEdit(self)
        #self.text_edit.setReadOnly(True)
        self.default_text_weight = self.text_edit.fontWeight()

        self.setCentralWidget(self.text_edit)

        self.name_formater= QtGui.QTextCharFormat()
        self.name_formater.setFontWeight(QtGui.QFont.DemiBold)
        self.name_formater.setForeground(QtCore.Qt.blue)
        self.name_formater.setFontPointSize(13)

        self.text_formater = QtGui.QTextCharFormat()
        self.text_formater.setFontWeight(self.text_edit.fontWeight())
        self.text_formater.setForeground(QtCore.Qt.black)
        self.text_formater.setFontPointSize(13)

    def _chat_formater(self, sender, message):
        self.text_edit.setTextColor(QtGui.QColor("red"))
        cursor = self.text_edit.textCursor()
        cursor.setCharFormat(self.name_formater)
        cursor.insertText(sender + ': ')

        cursor.setCharFormat(self.text_formater)
        cursor.insertText(message)
        cursor.insertBlock()

    @QtCore.pyqtSlot(str, str)
    def socket_chat_slot(self, sender, message):
        self._chat_formater(sender, message)

    @QtCore.pyqtSlot(QtCore.QByteArray)
    def chat_slot(self, qbyte_array):
        text = str(qbyte_array).split('\\r\\n')[12]
        text = text.split('&', maxsplit=2)

        host = text[0][5:]
        user = html.unescape(text[1][7:])
        message = html.unescape(text[2][8:][:-1])
        self._chat_formater(user, message)
