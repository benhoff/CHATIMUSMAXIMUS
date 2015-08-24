import os
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
        # tried to set the background to be transparent
        # does not work without a compositor in Linux
        self.setAttribute(Qt.WA_NoSystemBackground)
        self.setStyleSheet('background: transparent;')
        self.setAttribute(Qt.WA_TranslucentBackground)
        # Create the central widget
        self.central_widget = CentralWidget(parent=self)
        self.setCentralWidget(self.central_widget)

        self.status_bar = StatusBar(parent=self)
        self.setStatusBar(self.status_bar)

        self.central_widget.message_area.time_signal.connect(self.status_bar.time_label.setText)

    def set_settings(self, settings):
        for key, setting in settings.items():
            display_settings = setting['display_settings']
            if display_settings['display_missing']:
                self.status_bar.set_up_helper(key.title())
            if display_settings['text_color']:
                self.central_widget.message_area.set_color(display_settings['text_color'], key)
