import glob
from os import path
from PyQt5 import QtWidgets, QtGui
from chatimusmaximus.gui import CentralWidget, StatusBar, MenuBar
from chatimusmaximus.gui.models.settings_model import SettingsModel


def _get_icon_dict():
    icon_path = path.join(path.dirname(__file__), 'resources', 'icons', '')
    filepaths = glob.glob(str(icon_path) + '*.png')
    filenames = [path.basename(f).split('.')[0] for f in filepaths]
    file_platform = zip(filepaths, filenames)

    icon_dict = {name: QtGui.QImage(path) for (path, name) in file_platform}
    return icon_dict


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
        # duck type for easier access in `main`
        self.command_line_signal = self.central_widget.command_line_signal
        self.chat_slot = self.central_widget.chat_slot
        self.setCentralWidget(self.central_widget)

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

        icon_dict = _get_icon_dict()

        for platform, icon_path in icon_dict.items():
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
