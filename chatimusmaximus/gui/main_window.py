import os
from enum import Enum
from datetime import datetime
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt

class StatusBarSelector(Enum):
    Youtube = 0
    Twitch = 1
    Livecoding = 2
    WatchPeopleCode = 3

class MainWindow(QtWidgets.QMainWindow):
    _time_signal = QtCore.pyqtSignal(str)
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
        self.setAttribute(Qt.WA_NoSystemBackground)
        self.setStyleSheet('background: transparent;')
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.text_edit.setWindowFlags(Qt.FramelessWindowHint)
        self.text_edit.setAttribute(Qt.WA_TranslucentBackground)
        self.text_edit.viewport().setAutoFillBackground(False)

        vertical_layout = QtWidgets.QVBoxLayout()

        button = QtWidgets.QPushButton("CLEAR")
        button.setStyleSheet('color: white;')
        button.clicked.connect(self.text_edit.clear)

        vertical_layout.addWidget(self.text_edit)
        vertical_layout.addWidget(button)

        central_widget = QtWidgets.QWidget()
        central_widget.setLayout(vertical_layout)

        self.setCentralWidget(central_widget)

        # sets name and text formats
        self.name_format = None
        self.text_format = None
        self._file_dir = os.path.realpath(os.path.dirname(__file__))
        self._set_up_text_formats()
        self._status_widgets = []
        self._set_up_status_bar_helper()

    def _set_up_status_bar_helper(self):
        status_bar = QtWidgets.QStatusBar(parent=self)
        red_button = os.path.join(self._file_dir, 'resources', 'red_button.png')
        for platform in StatusBarSelector:
            button = QtWidgets.QPushButton(QtGui.QIcon(red_button), 
                                           ' ' + platform.name)

            button.setFlat(True)
            button.setAutoFillBackground(True)
            button.setStyleSheet('color: white;')
            status_bar.addPermanentWidget(button)
            self._status_widgets.append(button)
        time_label = QtWidgets.QLabel()
        time_label.setStyleSheet('color: white;')
        self._time_signal.connect(time_label.setText)
        status_bar.addPermanentWidget(time_label)
        self.setStatusBar(status_bar)

    def set_service_icon(self, service_index, bool):
        button = self._status_widgets[service_index]
        if bool:
            green_button = os.path.join(self._file_dir, 'resources', 'green_button.png')
            button.setIcon(QtGui.QIcon(green_button))
        else:
            red_button = os.path.join(self._file_dir, 'resources', 'red_button.png')
            button.setIcon(red_button)

    @QtCore.pyqtSlot(str, str, int)
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
        cursor.setCharFormat(self.name_formats[platform])
        # get the timestamp
        formatted_datetime = datetime.now().strftime("%H:%M:%S")
        self._time_signal.emit(formatted_datetime)
        # the platform name and timestamp are in a bracket. Example: `[YT@12:54:00]:`
        bracket_string = ' [{}]: '.format(StatusBarSelector(platform).name[0])
        # inserts the sender name next to the platform & timestamp
        cursor.insertText(sender + bracket_string)
        
        # sets format to text format
        cursor.setCharFormat(self.text_format)
        # inserts message
        cursor.insertText(message)
        # inserts newline
        cursor.insertBlock()
        cursor.movePosition(QtGui.QTextCursor.End, QtGui.QTextCursor.MoveAnchor)
        self.text_edit.setTextCursor(cursor)

    def _set_up_text_formats(self):
        """
        Helper method to create the name formater helpers
        `self.name_format` is used for names
        `self.test_formater` is used for the messages
        """
        self.name_formats = []
        for color in (Qt.red, Qt.darkMagenta, Qt.yellow, Qt.green):
            # name format is Demibold, blue, with size 13
            name_format = QtGui.QTextCharFormat()
            name_format.setFontWeight(QtGui.QFont.DemiBold)
            name_format.setForeground(color)
            name_format.setFontPointSize(13)
            self.name_formats.append(name_format)

        #text format is black, normal fontweight, and size 13
        self.text_format = QtGui.QTextCharFormat()
        self.text_format.setFontWeight(self.text_edit.fontWeight())
        self.text_format.setForeground(Qt.white)
        self.text_format.setFontPointSize(13)
