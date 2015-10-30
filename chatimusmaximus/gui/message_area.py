import re
from datetime import datetime
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import Qt


class _StandardTextFormat(QtGui.QTextCharFormat):
    """
    Standard text format for `MessageArea`
    """
    def __init__(self, text_color=Qt.white, font=QtGui.QFont.DemiBold):
        super(_StandardTextFormat, self).__init__()
        self.setFontWeight(font)
        self.setForeground(text_color)
        self.setFontPointSize(13)


class MessageArea(QtWidgets.QTextEdit):
    time_signal = QtCore.pyqtSignal(str)
    listeners_signal = QtCore.pyqtSignal(str, str)

    def __init__(self, parent=None):
        super(MessageArea, self).__init__(parent)
        self.setReadOnly(True)
        self.text_format = _StandardTextFormat(font=self.fontWeight())

        # styling
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.viewport().setAutoFillBackground(False)
        listener_color = _StandardTextFormat(QtGui.QColor('blue'))
        self.name_formats = {'listener': listener_color}

        self.listeners = []
        self.listeners_signal.connect(self.listeners_slot)
        self.listener_commands = ['!']

    def set_color(self, color, platform):
        QColor = QtGui.QColor
        if platform in self.name_formats:
            format = self.name_formats[platform]
            format.setForeground(QColor(color))
        else:
            self.name_formats[platform] = _StandardTextFormat(QColor(color))

    @QtCore.pyqtSlot(str, str)
    def listeners_slot(self, sender, message):
        # strip the first word off of the message
        # keep the trailing sentence intact
        try:
            cmd, message = message.split(' ', maxsplit=1)
        except ValueError:
            cmd = message.rstrip()
            message = None
        for arg in self.listener_commands:
            cmd = cmd.replace(arg, '')
        cmd = re.compile(cmd)
        result = None
        for listener in self.listeners:
            if cmd in listener.matches:
                try:
                    result = listener(cmd, message)
                except Exception as e:
                    result = str(e)
                break

        if result:
            self._insert_and_format('Vex', result, 'listener')

    @QtCore.pyqtSlot(str, str, str)
    def chat_slot(self, sender, message, platform):
        # get the timestamp
        formatted_datetime = datetime.now().strftime("%H:%M:%S")
        self.time_signal.emit(formatted_datetime)

        message = message.lstrip()
        self._insert_and_format(sender, message, platform)
        # get scroll bar and set to maximum
        scroll_bar = self.verticalScrollBar()
        scroll_bar.setValue(scroll_bar.maximum())
        if message[0] in self.listener_commands and self.listeners != []:
            self.listeners_signal.emit(sender, message)

    def _insert_and_format(self, sender, message, platform):
        """
        Helper method to handle the text display logic
        """
        # get cursor
        cursor = self.textCursor()
        # set the format to the name format
        cursor.setCharFormat(self.name_formats[platform])
        if not platform == 'listener':
            # the platform name is in a bracket. Example: `[Youtube]:`
            bracket_string = ' [{}]: '.format(platform.title())
        else:
            bracket_string = ': '
        if not cursor.atEnd():
            cursor.movePosition(QtGui.QTextCursor.End)
        # inserts the sender name next to the platform & timestamp
        cursor.insertText(sender + bracket_string)
        # sets format to text format
        cursor.setCharFormat(self.text_format)
        # inserts message
        cursor.insertText(message)
        # inserts newline
        cursor.insertBlock()
        self.setTextCursor(cursor)
