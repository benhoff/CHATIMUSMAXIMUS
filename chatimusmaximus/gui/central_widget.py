from PyQt5 import QtWidgets
from gui import MessageArea


class CentralWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(CentralWidget, self).__init__(parent)
        button = QtWidgets.QPushButton("CLEAR")
        button.setStyleSheet('color: white;')
        # create the text edit used to display the text
        self.message_area = MessageArea(parent=self)

        # duck type the slot onto the MainWindow for ease of access
        self.chat_slot = self.message_area.chat_slot

        # create `clear` button
        button.clicked.connect(self.message_area.clear)

        # create vertical layout to stack the textedit on top
        # of the `clear` button
        vertical_layout = QtWidgets.QVBoxLayout()

        # add the text edit and button to vertical layout
        vertical_layout.addWidget(self.message_area)
        vertical_layout.addWidget(button)
        self.setLayout(vertical_layout)
