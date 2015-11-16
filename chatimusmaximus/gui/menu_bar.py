import asyncio
from PyQt5 import QtWidgets, QtCore


class SettingsDialog(QtWidgets.QDialog):
    def __init__(self, model, parent=None):
        super().__init__(parent)
        layout = QtWidgets.QVBoxLayout()
        tree_view = QtWidgets.QTreeView()
        tree_view.setModel(model)
        layout.addWidget(tree_view)
        self.setLayout(layout)



class MenuBar(QtWidgets.QMenuBar):
    def __init__(self, settings_model, parent=None):
        super(MenuBar, self).__init__(parent)
        self.setStyleSheet('color: white;')
        file_menu = QtWidgets.QMenu('File', parent=self)
        file_menu.addAction('Settings')
        file_menu.addAction('Exit', self._stop_action_loop)
        self.addMenu(file_menu)
        self.settings_model = settings_model
    
    @QtCore.pyqtSlot()
    def _stop_action_loop(self):
        asyncio.get_event_loop().stop()

    @QtCore.pyqtSlot()
    def _launch_settings(self):
        dialog = SettingsDialog(self.settings_model)
        dialog.show()
