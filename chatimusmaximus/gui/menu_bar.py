import asyncio
from PyQt5 import QtWidgets, QtCore


class SettingsDialog(QtWidgets.QDialog):
    def __init__(self, model, parent=None):
        super().__init__(parent)
        self.setWindowTitle('CHATIMUS Settings')
        self.setStyleSheet('background: black; color: white;')
        ok_button = QtWidgets.QPushButton('Ok')
        ok_button.setDefault(True)
        cancel_button = QtWidgets.QPushButton('Cancel')
        apply_button = QtWidgets.QPushButton('Apply')
        layout = QtWidgets.QVBoxLayout()
        tree_view = QtWidgets.QTreeView()
        # tree_view.setHeaderHidden(True)
        tree_view.setModel(model)
        tree_view.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectItems)
        tree_view.setUniformRowHeights(True)
        tree_view.setAnimated(False)
        tree_view.setAllColumnsShowFocus(True)

        tree_view.resizeColumnToContents(0)
        layout.addWidget(tree_view)

        horizontal_button_widget = QtWidgets.QWidget()
        horizontal_layout = QtWidgets.QHBoxLayout()
        horizontal_layout.addWidget(ok_button)
        horizontal_layout.addWidget(cancel_button)
        horizontal_layout.addWidget(apply_button)
        horizontal_button_widget.setLayout(horizontal_layout)

        layout.addWidget(horizontal_button_widget)

        ok_button.clicked.connect(self.done)
        cancel_button.clicked.connect(self.reject)
        # TODO: add in apply button connection

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
