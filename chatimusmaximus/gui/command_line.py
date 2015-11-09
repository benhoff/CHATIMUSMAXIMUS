from PyQt5 import QtWidgets, QtCore


class LineEdit(QtWidgets.QLineEdit):
    listener_signal = QtCore.pyqtSignal(str, str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.returnPressed.connect(self.return_pressed_slot)
        self.setStyleSheet('color: white; font: demibold; font-size: 18px; border: 0px solid black;')

    @QtCore.pyqtSlot()
    def return_pressed_slot(self):
        # TODO: emit a platform
        self.listener_signal.emit('', self.text())
        self.clear()


class CommandLine(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        prompt = 'user@chatimus ~$'

        self.button = QtWidgets.QPushButton(prompt)
        self.button.setStyleSheet('color: white; font: bold; outline: none; font-size: 18px;')
        # TODO: intergrate into stylesheet
        self.button.setFlat(True)

        self.line_edit = LineEdit()
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.button)
        layout.addWidget(self.line_edit)
        layout.setSpacing(0)
        self.setLayout(layout)

        self.listener_signal = self.line_edit.listener_signal
        self.button.clicked.connect(self.give_focus)

    def set_settings(self, settings):
        prompt = settings['command_line']
        if not prompt == str():
            self.button.setText(prompt)

    def give_focus(self):
        self.line_edit.setFocus()