import html, json
from enum import Enum
from datetime import datetime
from PyQt5 import QtWidgets, QtCore, QtGui

class StatusBarSelector(Enum):
    Youtube = 0
    Twitch = 1
    Livecoding = 2
    WatchPeopleCode = 3

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

        vertical_layout = QtWidgets.QVBoxLayout()

        button = QtWidgets.QPushButton("CLEAR")
        button.clicked.connect(self.text_edit.clear)

        vertical_layout.addWidget(self.text_edit)
        vertical_layout.addWidget(button)

        central_widget = QtWidgets.QWidget()
        central_widget.setLayout(vertical_layout)

        self.setCentralWidget(central_widget)

        # sets name and text formats
        self.name_format = None
        self.text_format = None
        self._set_up_text_formats()
        self._status_widgets = []
        self._set_up_status_bar_helper()

    def _set_up_status_bar_helper(self):
        status_bar = QtWidgets.QStatusBar(parent=self)
        red_button = 'gui/resources/red_button.png'
        for platform in StatusBarSelector:
            button = QtWidgets.QPushButton(QtGui.QIcon(red_button), 
                                           ' ' + platform.name)

            button.setFlat(True)
            button.setAutoFillBackground(True)
            status_bar.addWidget(button)
            self._status_widgets.append(button)

        self.setStatusBar(status_bar)

    def set_service_icon(self, service_index, bool):
        button = self._status_widgets[service_index]
        if bool:
            green_button = 'gui/resources/green_button.png'
            button.setIcon(QtGui.QIcon(green_button))
        else:
            red_button = 'gui/resources/red_button.png'
            button.setIcon(red_button)

    @QtCore.pyqtSlot(str, str, str)
    def chat_string_slot(self, sender, message, platform):
        self._chat_formater(sender, message, platform)
        self.text_edit.verticalScrollBar().setValue(
                self.text_edit.verticalScrollBar().maximum())

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
