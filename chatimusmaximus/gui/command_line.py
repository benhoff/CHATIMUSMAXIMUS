from PyQt5 import QtWidgets, QtCore


class LineEdit(QtWidgets.QLineEdit):
    listener_signal = QtCore.pyqtSignal(str, str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.returnPressed.connect(self.return_pressed_slot)
        self.setStyleSheet('color: white; font: demibold')
        self.setAttribute(QtCore.Qt.WA_MacShowFocusRect, 0)

    @QtCore.pyqtSlot()
    def return_pressed_slot(self):
        self.listener_signal.emit('', self.text())
        self.clear()

class CommandLine(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.prompt = 'user@chatimus ~$'
        label = QtWidgets.QPushButton(self.prompt)
        label.setStyleSheet('color: white; font: demibold')
        self.line_edit = LineEdit()
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(label)
        layout.addWidget(self.line_edit)
        layout.setContentsMargins(-1, -1, -1, 0)
        self.setLayout(layout)
        self.listener_signal = self.line_edit.listener_signal
        label.clicked.connect(self.give_focus)

    def give_focus(self):
        self.line_edit.setFocus()
