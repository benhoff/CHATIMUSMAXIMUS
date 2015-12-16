from collections import OrderedDict
from PyQt5 import QtCore
from PyQt5.QtCore import Qt


class SettingsModel(QtCore.QAbstractItemModel):
    command_prompt_signal = QtCore.pyqtSignal(str)
    # website name, color
    set_text_color_signal = QtCore.pyqtSignal(str, str)
    # website name, args
    instantiate_website = QtCore.pyqtSignal(str, list)
    # website name, activate/deactivate
    manage_website_state = QtCore.pyqtSignal(str, bool)
    show_website_missing = QtCore.pyqtSignal(str, bool)

    def __init__(self, data, parent=None):
        super().__init__(parent)
        self.root = data
        self.my_index = {}   # Needed to stop garbage collection

    def index(self, row, column, parent):
        """Returns QModelIndex to row, column in parent (QModelIndex)"""
        if not self.hasIndex(row, column, parent):
            return QtCore.QModelIndex()
        if parent.isValid():
            index_pointer = parent.internalPointer()
            parent_dict = self.root[index_pointer]
        else:
            parent_dict = self.root
            index_pointer = ()
        row_key = list(parent_dict.keys())[row]
        child_pointer = (index_pointer, row_key)
        try:
            child_pointer = self.my_index[child_pointer]
        except KeyError:
            self.my_index[child_pointer] = child_pointer
        index = self.createIndex(row, column, child_pointer)
        return index

    def setData(self, index, value, role=Qt.EditRole):
        pointer = self.my_index[index.internalPointer()]
        self.root[pointer] = value
        self.dataChanged.emit(index, index)
        return True

    def flags(self, index):
        if not index.isValid():
            return 0

        return Qt.ItemIsEditable | Qt.ItemIsEnabled | Qt.ItemIsSelectable


    def get_row(self, key):
        """Returns the row of the given key (list of keys) in its parent"""
        if key:
            parent = key[:-1]
            if not parent:
                return 0
            return list(self.root[parent].keys()).index(key[-1])
        else:
            return 0

    def parent(self, index):
        """
        Returns the parent (QModelIndex) of the given item (QModelIndex)
        Top level returns QModelIndex()
        """
        if not index.isValid():
            return QtCore.QModelIndex()
        child_key_list = index.internalPointer()
        if child_key_list:
            parent_key_list = child_key_list[:-1]
            try:
                parent_key_list = self.my_index[parent_key_list]
            except KeyError:
                self.my_index[parent_key_list] = parent_key_list
            return self.createIndex(self.get_row(parent_key_list), 0,
                                    parent_key_list)
        else:
            return QtCore.QModelIndex()

    def rowCount(self, parent):
        """Returns number of rows in parent (QModelIndex)"""
        if parent.column() > 0:
            return 0    # only keys have children, not values
        if parent.isValid():
            indexPtr = parent.internalPointer()
            parentValue = self.root[indexPtr]
            if isinstance(parentValue, OrderedDict):
                return len(self.root[indexPtr])
            else:
                return 0
        else:
            return len(self.root)

    def columnCount(self, parent):
        return 2  # Key & value

    def data(self, index, role):
        """Returns data for given role for given index (QModelIndex)"""
        if not index.isValid():
            return None
        if role in (Qt.DisplayRole, Qt.EditRole):
            indexPtr = index.internalPointer()
            if index.column() == 1:    # Column 1, send the value
                if role == Qt.EditRole:
                    print(index.column(), self.root[indexPtr])
                return self.root[indexPtr]
            else:                   # Column 0, send the key
                if indexPtr:
                    return indexPtr[-1]
                else:
                    return None
        else:  # Not display or Edit
            return None
