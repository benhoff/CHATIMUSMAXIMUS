from os import path
from PyQt5 import QtWidgets, QtGui
from chatimusmaximus.gui import CentralWidget, StatusBar, MenuBar
from chatimusmaximus.gui.models.settings_model import SettingsModel

_icon_path = path.join(path.dirname(__file__), 'resources', 'icons')
_str = '{}.png'
_platforms = ('youtube', 'watchpeoplecode', 'twitch', 'livecoding')
_ICON_DICT = {x: path.join(_icon_path, _str.format(x)) for x in _platforms}
for platform, path_ in _ICON_DICT.items():
    _ICON_DICT[platform] = QtGui.QImage(path_)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, settings: dict=None, parent=None):
        """
        MainWindow uses a QTextEdit to display chat
        """
        # initialize parent class. Req'd for PyQt subclasses
        super().__init__(parent)
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

        self.settings_model = SettingsModel()
        self._set_settings(self.settings_model.root)

        # alias for pep8
        msg_area = self.central_widget.message_area
        msg_area.time_signal.connect(self.status_bar.time_label.setText)
        self.menu_bar = MenuBar(parent=self)
        self.setMenuBar(self.menu_bar)

        for platform, icon_path in _ICON_DICT.items():
            msg_area.set_icon(icon_path, platform)

    def _set_settings(self, settings):
        # FIXME: not used
        # display = settings.get('display')
        for service, platform in settings['services'].items():
            if not service == 'youtube':
                for platform_name, settings in platform.items():
                    if settings['display_missing']:
                        self.status_bar.set_up_helper(platform_name.title())
            else:
                if platform['display_missing']:
                    self.status_bar.set_up_helper(service.title())

    def set_command_prompt(self, prompt):
        self.central_widget.command_line.button.setText(prompt)
