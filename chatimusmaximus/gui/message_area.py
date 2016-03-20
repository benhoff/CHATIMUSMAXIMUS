from os import path
import re
from datetime import datetime
from PyQt5 import QtWidgets, QtGui, QtCore, QtMultimedia
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
        self.setVerticalAlignment(QtGui.QTextCharFormat.AlignMiddle)


# TODO: see `QTextEdit.setAlignment` for setting the time to the right
class MessageArea(QtWidgets.QTextEdit):
    time_signal = QtCore.pyqtSignal(str)
    listeners_signal = QtCore.pyqtSignal(str, str)

    def __init__(self, parent=None):
        super(MessageArea, self).__init__(parent)
        self.setReadOnly(True)
        self.sender_format = _StandardTextFormat(Qt.gray, self.fontWeight())
        self.time_format = _StandardTextFormat(Qt.gray, self.fontWeight())
        self.text_format = _StandardTextFormat()

        # styling
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.viewport().setAutoFillBackground(False)
        self.name_formats = {}

        self.listeners = []
        self.listeners_signal.connect(self.listeners_slot)
        self.listener_commands = ['!']
        sound_filepath = path.join(path.dirname(__file__),
                                   'resources',
                                   'click.wav')

        # sound_filepath = path.abspath(sound_filepath)
        sound_filepath = QtCore.QUrl.fromLocalFile(sound_filepath)

        self.sound = QtMultimedia.QSoundEffect()
        self.sound.setSource(sound_filepath)
        self.sound.setVolume(0.5)
        self.sound.setLoopCount(1)

    def set_settings(self, settings_model):
        settings_model.create_platform.connect(self.set_color)

    def set_icon(self, icon, platform):
        document = self.document()
        document.addResource(QtGui.QTextDocument.ImageResource,
                             QtCore.QUrl(platform),
                             icon)

    def set_font(self, font):
        self.text_format.setFont(font)

    @QtCore.pyqtSlot(str, str)
    def listeners_slot(self, sender, message):
        # strip the first word off of the message
        # keep the trailing sentence intact
        if sender == 'command_line':
            self._insert_and_format('User', message, 'listener')

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
    def chat_slot(self, platform, sender, message):
        # get the timestamp
        formatted_datetime = datetime.now().strftime("%H:%M:%S")
        self.time_signal.emit(formatted_datetime)

        message = message.lstrip()
        self._insert_and_format(sender, message, platform)
        self.sound.play()
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
        if not cursor.atEnd():
            cursor.movePosition(QtGui.QTextCursor.End)
        # inserts the sender name next to the platform & timestamp
        if not platform == 'listener':
            cursor.insertImage(platform)
        cursor.setCharFormat(self.sender_format)
        cursor.insertText(' {}'.format(sender))
        cursor.insertBlock()
        cursor.setCharFormat(self.text_format)
        cursor.insertText(message)
        # inserts newline
        cursor.insertBlock()
        self.setTextCursor(cursor)
