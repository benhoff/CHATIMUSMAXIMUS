import asyncio
from PyQt5 import QtWidgets, QtCore

class SettingsDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)



class MenuBar(QtWidgets.QMenuBar):
    def __init__(self, parent=None):
        super(MenuBar, self).__init__(parent)
        self.setStyleSheet('color: white;')
        file_menu = QtWidgets.QMenu('File', parent=self)
        file_menu.addAction('Settings')
        file_menu.addAction('Exit', self._stop_action_loop)
        self.addMenu(file_menu)
    
    @QtCore.pyqtSlot()
    def _stop_action_loop(self):
        asyncio.get_event_loop().stop()

    @QtCore.pyqtSlot()
    def _launch_settings(self):
        dialog = QtWidgets.QDi
