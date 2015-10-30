from PyQt5 import QtWidgets
from .message_area import MessageArea
from .command_line import CommandLine


class CentralWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(CentralWidget, self).__init__(parent)
        # create the text edit used to display the text
        self.message_area = MessageArea(parent=self)

        # duck type the slot onto the MainWindow for ease of access
        self.chat_slot = self.message_area.chat_slot

        command_line = CommandLine(parent=self)
        command_line.listener_signal.connect(self.message_area.listeners_slot)

        # create vertical layout to stack the textedit on top
        # of the `clear` button
        vertical_layout = QtWidgets.QVBoxLayout()

        # add the text edit and button to vertical layout
        vertical_layout.addWidget(self.message_area)
        vertical_layout.addWidget(command_line)
        vertical_layout.setContentsMargins(-1, -1, -1, 0)
        self.setLayout(vertical_layout)
