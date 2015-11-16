import asyncio
from PyQt5 import QtWidgets, QtCore
import yaml

with open(filepath) as file_:
    settings = yaml.load(file_)



def _to_list(object):
    if isinstance(object, basestring):
        return [object]
    elif hasattr(object, '__iter__'):
        return [x for x in object]
    else:
        return [object]

class TreeItem(object):
    def __init__(self, data, parent=None, children=None):
        super().__init__()
        self.parent = parent
        self.item_data = _to_list(data)
        self.children = _to_list(children)

    def appendChild(self, child):
        self.children.append(child)

    def childCount(self):
        return len(self.children)

    def columnCount(self):
        return len(self.item_data)

    def data(self, column):
        return self.item_data[column]

    def row(self):
        if self.parent:
            return self.parent.children.index(self)
        else:
            return 0
def _return_tree(value, parent=None):
    if isinstance(value, dict):
        childs = []
        for key, value in value.keys():
            value = _return_tree(value.keys()[0], value.values())
        result = TreeItem(key, parent, value)
        value.parent = result
        return result
    else:
        return TreeItem(value, parent)


class SettingsData(TreeItem):
    def __init__(self, dictionary: dict):
        super().__init__(None)
        self.root = self
        settings_root = TreeItem('Settings', parent=self)
        self.appendChild(settings_root)
        # youtube, values could be a dict
        for key, value in dictionary.items():
            top_level = TreeItem(key, self)
            children = _return_tree(value, top_level)
            top_level.children.extend(children)
            self.appendChild(top_level)


class SettingsModel(QtCore.QAbstractItemModel):
    def __init__(self, data=None, parent=None):
        super().__init__(parent)
        self._data = data

    def index(self, row, column, parent=QtCore.QModelIndex()):
        if not self.hasIndex(row, column, parent):
            return QtCore.QModelIndex()

        if not parent.isValid():
            parent_item = self.data_.root
        else:
            parent_item = parent.internalPointer()

        child_item = parent_item.child(row)

        if child_item:
            return self.createIndex(row, column, childItem)
        else:
            return QtCore.QModelIndex()

    def flags(self, index):
        pass

    def setData(self, index, value, role=QtCore.Qt.EditRole):
        if not value.isValid():
            return False

    def parent(self, index):
        if not index.isValid():
            return QtCore.QModelIndex()

        child_item = index.internalPointer()
        if not child_item:
            return QtCore.QModelIndex()

        parent_item = child_item.parent
        
        # TODO: verify if this works
        if parent_item = self.data_.root:
            return QtCore.QModelIndex()
    
        # TODO: verify that this works
        return self.createIndex(parent_item.row(), 0, parent_item)

    def rowCount(self, parent=QtCore.QModelIndex()):
        if parent.column() > 0:
            return True
        if not parent.isValid():
            parent_item = self.data_.root
        else:
            parent_item = parent.internalPointer()
        return parent_item.childCount()

    def columnCount(self, parent=QtCore.QModelIndex()):
        if parent and parent.isValid():
            return parent.internalPointer().columnCount()
        else:
            return 1

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if not index.isValid():
            return

        item = index.internalPointer()

        if not role == QtCore.Qt.DisplayRole:
            return

        return item.data(index.column())
