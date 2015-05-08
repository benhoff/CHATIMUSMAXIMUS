from PyQt5 import QtWidgets, QtCore, QtGui

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setWindowTitle("CHATIMUSMAXIMUS")
        self.text_edit = QtWidgets.QTextEdit(self)
        #self.text_edit.setReadOnly(True)
        self.default_text_weight = self.text_edit.fontWeight()
        print(self.text_edit.textColor().name())

        self.setCentralWidget(self.text_edit)

        self.name_formater= QtGui.QTextCharFormat()
        self.name_formater.setFontWeight(QtGui.QFont.DemiBold)
        self.name_formater.setForeground(QtCore.Qt.blue)
        self.name_formater.setFontPointSize(13)

        self.text_formater = QtGui.QTextCharFormat()
        self.text_formater.setFontWeight(self.text_edit.fontWeight())
        self.text_formater.setForeground(QtCore.Qt.black)
        self.text_formater.setFontPointSize(13)


    @QtCore.pyqtSlot(QtCore.QByteArray)
    def chat_slot(self, qbyte_array):
        text = str(qbyte_array)
        self.text_edit.setTextColor(QtGui.QColor("red"))
        cursor = self.text_edit.textCursor()
        cursor.setCharFormat(self.name_formater)
        cursor.insertText(text)

        cursor.setCharFormat(self.text_formater)
        cursor.insertText("Boogly, boogly")
