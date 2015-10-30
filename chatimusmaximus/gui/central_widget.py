from PyQt5 import QtWidgets, QtCore
from gui import MessageArea


class LineEdit(QtWidgets.QLineEdit):
    listener_signal = QtCore.pyqtSignal(str, str)
    def __init__(self, parent=None):
        super().__init__(parent)
        self.returnPressed.connect(self.return_pressed_slot)
        self.setStyleSheet('border: 1px solid white; text_color: white')

    @QtCore.pyqtSlot()
    def return_pressed_slot(self):
        self.listener_signal.emit('', self.text())
        self.clear()


class CentralWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(CentralWidget, self).__init__(parent)
        # create the text edit used to display the text
        self.message_area = MessageArea(parent=self)

        # duck type the slot onto the MainWindow for ease of access
        self.chat_slot = self.message_area.chat_slot

        line_edit = LineEdit(parent=self)
        line_edit.listener_signal.connect(self.message_area.listeners_slot)

        # create vertical layout to stack the textedit on top
        # of the `clear` button
        vertical_layout = QtWidgets.QVBoxLayout()

        # add the text edit and button to vertical layout
        vertical_layout.addWidget(self.message_area)
        vertical_layout.addWidget(line_edit)
        self.setLayout(vertical_layout)
