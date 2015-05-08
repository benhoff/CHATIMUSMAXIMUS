from PyQt5 import QtWidgets, QtCore

class MainWindow(QtWidgets.QMainWindow):
    chat_signal = QtCore.pyqtSignal(str)
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setWindowTitle("CHATIMUSMAXIMUS")
        self.text_edit = QtWidgets.QTextEdit(self)
        self.chat_signal.connect(self.text_edit.append)
        self.text_edit.setReadOnly(True)

        self.setCentralWidget(self.text_edit)


    @QtCore.pyqtSlot(QtCore.QByteArray)
    def chat_slot(self, qbyte_array):
        self.chat_signal.emit(str(qbyte_array))


