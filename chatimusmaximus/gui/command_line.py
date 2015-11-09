from PyQt5 import QtWidgets, QtCore


class LineEdit(QtWidgets.QLineEdit):
    listener_signal = QtCore.pyqtSignal(str, str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.returnPressed.connect(self.return_pressed_slot)
        self.setStyleSheet('color: white; font: demibold; font-size: 18px; border: 0px solid black;')

    @QtCore.pyqtSlot()
    def return_pressed_slot(self):
        self.listener_signal.emit('', self.text())
        self.clear()


class CommandLine(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        prompt = 'user@chatimus ~$'

        self.label = QtWidgets.QPushButton(prompt)
        self.label.setStyleSheet('color: white; font: bold; font-size: 18px;')

        self.line_edit = LineEdit()
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.line_edit)
        layout.setSpacing(0)
        self.setLayout(layout)

        self.listener_signal = self.line_edit.listener_signal
        self.label.clicked.connect(self.give_focus)

    def set_settings(self, settings):
        prompt = settings['command_line']
        if not prompt == str():
            self.label.setText(prompt)

    def give_focus(self):
        self.line_edit.setFocus()
