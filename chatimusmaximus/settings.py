from PyQt5 import QtWidgets, QtCore
import yaml


class SettingsModel(QtCore.QAbstractItemModel):
    def __init__(self, parent=None):
        super().__init__(parent)

    def index(self, row, column, parent=QtCore.QModelIndex()):
        pass

    def parent(self, index):
        pass

    def rowCount(self, parent=QtCore.QModelIndex()):
        pass

    def columnCount(self, parent=QtCore.QModelIndex()):
        pass

    def data(self, index, role=QtCore.Qt.DisplayRole):
        pass


class Settings(QtCore.QObject):
    # platform, key, value
    settings_changed = QtCore.pyqtSignal(str, str, str)
    def __init__(self, filepath=None, parent=None):
        super().__init__(parent)
        self.filepath = filepath 
        self.settings = None

    def __setitem__(self, key, item):
        pass

    def __getitem__(self, key):
        pass

    def __len__(self):
        pass

    def __delitem__(self, key):
        pass

    def __contains__(self, item):
        pass

    def pop(self, *args):
        pass

    def load(self):
        pass
    
    def keys(self):
        pass

    def values(self):
        pass

    def items(self):
        pass

    def settings_changed(self):
        pass
