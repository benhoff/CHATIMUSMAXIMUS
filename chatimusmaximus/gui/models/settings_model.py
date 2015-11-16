from PyQt5 import QtCore


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
        if parent_item == self.data_.root:
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
