from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from gui import CentralWidget, StatusBar


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        """
        MainWindow uses a QTextEdit to display chat
        """
        # initialize parent class. Req'd for PyQt subclasses
        super(MainWindow, self).__init__(parent)
        # set title window to `CHATIMUSMAXIMUS`
        self.setWindowTitle("CHATIMUSMAXIMUS")
        self.setStyleSheet('background: black;')
        # Create the central widget
        self.central_widget = CentralWidget(parent=self)
        self.setCentralWidget(self.central_widget)

        self.status_bar = StatusBar(parent=self)
        self.setStatusBar(self.status_bar)

        # alias for pep8
        msg_area = self.central_widget.message_area
        msg_area.time_signal.connect(self.status_bar.time_label.setText)

    def set_settings(self, settings):
        # alias for pep8
        msg_area = self.central_widget.message_area

        display = settings.pop('display')
        message_color = display.get('text_color', 'blue')
        msg_area.set_color(message_color, 'listener')
        self.central_widget.set_settings(display)
        for key, setting in settings.items():
            display_settings = setting['display_settings']
            if display_settings['display_missing']:
                self.status_bar.set_up_helper(key.title())
            if display_settings['text_color']:
                # alias for pep8
                msg_area = self.central_widget.message_area
                msg_area.set_color(display_settings['text_color'], key)
