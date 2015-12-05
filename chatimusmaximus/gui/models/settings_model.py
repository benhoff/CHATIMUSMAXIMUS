from collections import OrderedDict
from PyQt5 import QtCore


class Wrapper(object):
    __slots__ = ('data', 'parent', 'index')
    def __init__(self, data, parent, index=None):
        self.data = data
        self.parent = parent
        self.index = index

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
        # wrappers stores references to all `Wrapper` instances so 
        # we don't garbage collect them
        self.indexes = {}

    def index(self, row, column, parent=QtCore.QModelIndex()):
        if not self.hasIndex(row, column, parent):
            return QtCore.QModelIndex()

        if parent.isValid():
            parent_item = parent.internalPointer()
        else:
            parent_item = self.root
        row_key = list(parent_item.keys())[row]
        child = parent_item + (row_key,)
        try:
            child =  self.indexes[child]
        except KeyError:
            self.indexes[child] = child
        index = self.createIndex(row, column, child)
        return index

    def flags(self, index):
        flags = super().flags(index)
        return flags

    def setData(self, index, value, role=QtCore.Qt.EditRole):
        pass

    def parent(self, index):
        if not index.isValid():
            return QtCore.QModelIndex()

        child_item = index.internalPointer()
        parent_key_list = child_item[:-1]
        try:
            parent = self.indexes[parent_key_list]
        except KeyError:
            self.indexes[parent_key_list] = parent_key_list
        parent_item = child_item.parent
        column = index.column()
        if isinstance(child_item, Wrapper):
            child_item = child_item.data
            column = 0
        if column == 0:
            row = list(parent_item.keys()).index(child_item)
        elif column == 1:
            row = list(parent_item.values()).index(child_item)
        else:
            print("""column value not handeled in `parent` function in {}
                    for {}""".format('SettingsModel', self))

        index = self.createIndex(row, 0, parent_item)
        parent_item.index = index
        return index

    def rowCount(self, parent=QtCore.QModelIndex()):
        if not parent.isValid():
            parent_item = self.root
        else:
            parent_item = parent.internalPointer()
        if isinstance(parent_item, OrderedDict):
            row = len(parent_item.values())
        else:
            row = 0
        return row

    def columnCount(self, parent=QtCore.QModelIndex()):
        if not parent.isValid():
            parent_item = self.root
        else:
            parent_item = parent.internalPointer()
        if isinstance(parent_item, Wrapper):
            return 1
        elif isinstance(parent_item, OrderedDict):
            return 2
        else:
            return 0

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if not index.isValid():
            return
        if not role == QtCore.Qt.DisplayRole and not role == QtCore.Qt.EditRole:
            return
        column = index.column()
        item = index.internalPointer()
        if isinstance(item, Wrapper):
            if column == 0:
                return item.data
            else:
                return None
        row = index.row()
        key = list(item.keys())[row]
        print(row, key, column)
        if column == 0:
            return key
        elif column == 1:
            value = item[key]
            return value
        else:
            print('column value in data is: {}'.format(column))
