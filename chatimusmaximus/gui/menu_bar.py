import asyncio
from PyQt5 import QtWidgets, QtCore


class SettingsDialog(QtWidgets.QDialog):
    def __init__(self, model, parent=None):
        super().__init__(parent)
        self.setWindowTitle('CHATIMUS Settings')
        ok_button = QtWidgets.QPushButton('Ok')
        cancel_button = QtWidgets.QPushButton('Cancel')
        apply_button = QtWidgets.QPushButton('Apply')
        layout = QtWidgets.QVBoxLayout()
        tree_view = QtWidgets.QTreeView()
        tree_view.setHeaderHidden(True)
        tree_view.setModel(model)
        tree_view.resizeColumnToContents(0)
        layout.addWidget(tree_view)
        layout.addWidget(ok_button)
        layout.addWidget(cancel_button)
        layout.addWidget(apply_button)
        

        ok_button.clicked.connect(self.done)
        apply_button.clicked.connect(self.accept)
        cancel_button.clicked.connect(self.reject)
        
        self.setLayout(layout)



class MenuBar(QtWidgets.QMenuBar):
    def __init__(self, settings_model=None, parent=None):
        super(MenuBar, self).__init__(parent)
        self.setStyleSheet('color: white;')
        file_menu = QtWidgets.QMenu('File', parent=self)
        file_menu.addAction('Settings', self._launch_settings)
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
        dialog.raise_()
        dialog.activateWindow()
