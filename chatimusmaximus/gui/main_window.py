from PyQt5 import QtWidgets
from gui import CentralWidget, StatusBar, MenuBar


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, settings: dict=None, parent=None):
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

        # add chat_slot to class
        self.chat_slot = self.central_widget.chat_slot

        self.status_bar = StatusBar(parent=self)
        self.set_widget_state = self.status_bar.set_widget_status
        self.setStatusBar(self.status_bar)

        # alias for pep8
        msg_area = self.central_widget.message_area
        msg_area.time_signal.connect(self.status_bar.time_label.setText)
        self.menu_bar = MenuBar(parent=self)
        self.setMenuBar(self.menu_bar)

    def set_settings(self, settings):
        display = settings.get('display')
        message_color = display.get('text_color', 'blue')
        self.set_color('listener', message_color)
        self.central_widget.set_settings(display)
        for key, setting in settings.items():
            if key == 'display':
                continue
            if setting['display_missing']:
                self.status_bar.set_up_helper(key.title())
            if display_settings['text_color']:
                self.set_color(key, display_settings['text_color'])

    @property
    def settings_model(self):
        return self._settings_model

    @settings_model.setter
    def settings_model(self, model):
        self._settings_model = model
        self.menu_bar.settings_model = model

    def set_color(self, platform, text_color):
        msg = self.central_widget.message_area
        msg.set_color(text_color, platform)

    def set_command_prompt(self, prompt):
        self.central_widget.command_line.button.setText(prompt)
