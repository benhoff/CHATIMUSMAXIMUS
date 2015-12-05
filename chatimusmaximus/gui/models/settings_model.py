from collections import OrderedDict
from PyQt5 import QtCore


class SettingsModel(QtCore.QAbstractItemModel):
    command_prompt_signal = QtCore.pyqtSignal(str)
    # website name, color
    set_text_color_signal = QtCore.pyqtSignal(str, str)
    # website name, args
    instantiate_website = QtCore.pyqtSignal(str, list)
    # website name, activate/deactivate
    manage_website_state = QtCore.pyqtSignal(str, bool)
    show_website_missing = QtCore.pyqtSignal(str, bool)

    def __init__(self, root_data=None, parent=None):
        super().__init__(parent)
        self.root = root_data
        self.root.parent = object()

    def index(self, row, column, parent=QtCore.QModelIndex()):
        if not self.hasIndex(row, column, parent):
            return QtCore.QModelIndex()

        if not parent.isValid():
            parent_item = self.root
            key = list(parent_item.keys())[row]
            if column == 1:
                child = parent_item[key]
            else:
                child = key
            if isinstance(child, str):
                child = parent_item
            else:
                return QtCore.QModelIndex()
        else:
            parent_item = parent.internalPointer()
            child = list(parent_item.values())[row]
            print(child, row, column)

        if child:
            index = self.createIndex(row, column, child)
            print(id(index))
            child.index = index
            return index
        else:
            return QtCore.QModelIndex()

    def flags(self, index):
        flags = super().flags(index)
        if not index.isValid():
            return flags
        item = index.internalPointer()
        try:
            if not item.item_flags:
                return flags
            else:
                return item.item_flags[index.column()]
        except AttributeError:
            return flags

    def setData(self, index, value, role=QtCore.Qt.EditRole):
        pass

    def parent(self, index):
        if not index.isValid():
            return QtCore.QModelIndex()

        child_item = index.internalPointer()
        if child_item == self.root:
            return QtCore.QModelIndex()

        parent_item = child_item.parent
        row = list(parent_item.values()).index(child_item)

        index = self.createIndex(row, 0, parent_item)
        parent_item.index = index
        return index

    def rowCount(self, parent=QtCore.QModelIndex()):
        if parent.column() > 0:
            return True
        if not parent.isValid():
            parent_item = self.root
        else:
            parent_item = parent.internalPointer()
        return len(parent_item.values())

    def columnCount(self, parent=QtCore.QModelIndex()):
        if parent.column() > 0:
            return 0
        return 2

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if not index.isValid():
            return
        if not role == QtCore.Qt.DisplayRole and not role == QtCore.Qt.EditRole:
            return
        row = index.row()
        column = index.column()
        item = index.internalPointer()
        print(row, column, 'in data', item.keys(), len(item.keys()), id(index))
        if row == len(item.keys()):
            row = row - 1

        key = list(item.keys())[row]
        if column == 0:
            return key 
        else:
            value = item[key]
            if isinstance(value, OrderedDict):
                return None
            else:
                return value
