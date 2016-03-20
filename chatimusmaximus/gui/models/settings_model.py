import argparse
from os import path
from operator import itemgetter
from collections import OrderedDict
import yaml

from PyQt5 import QtCore
from PyQt5.QtCore import Qt


class _OrderedLoader(yaml.Loader):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


def _construct_mapping(loader, node):
    loader.flatten_mapping(node)
    result = OrderedDict(sorted(loader.construct_pairs(node),
                                key=itemgetter(0)))

    return result


_OrderedLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
                               _construct_mapping)


def _validate_settings_not_blank(setting):
    settings_have_values = False
    for key, value in setting.items():
        if value == str() or key == 'display_settings' or key == 'connect':
            pass
        else:
            settings_have_values = True
            break
    return settings_have_values


def _append_parent_attribute(data: OrderedDict):
    for child in data.values():
        if isinstance(child, OrderedDict):
            child.parent = data
            _append_parent_attribute(child)


class SpecialDict(OrderedDict):
    def __init__(self, *args, **kwargs):
        super().__init__(sorted(kwargs.items()))

    def __getitem__(self, index):
        if isinstance(index, tuple):
            item = self
            for key in index:
                if item != ():
                    item = item[key]
            return item
        else:
            return super().__getitem__(index)

    def __setitem__(self, key, value):
        if isinstance(key, tuple):
            item = self
            previous_item = None
            for k in key:
                if item != ():
                    previous_item = item
                    item = item[k]
            previous_item[key[-1]] = value
        else:
            return super().__setitem__(key, value)


class SettingsModel(QtCore.QAbstractItemModel):
    command_prompt_signal = QtCore.pyqtSignal(str)
    # website name, color
    set_text_color_signal = QtCore.pyqtSignal(str, str)
    # website name, args
    instantiate_website = QtCore.pyqtSignal(str, list)
    # website name, activate/deactivate
    manage_website_state = QtCore.pyqtSignal(str, bool)
    show_website_missing = QtCore.pyqtSignal(str, bool)

    def __init__(self, data=None, parent=None):
        super().__init__(parent)
        if data is None:
            data = self._get_settings_helper()
            _append_parent_attribute(data)
        self.root = data
        self.my_index = {}   # Needed to stop garbage collection

    def _get_args(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--settings_path',
                            nargs='?',
                            action='store')

        return parser.parse_args()

    def _get_settings_helper(self):
        main_dir = path.dirname(path.realpath(__file__))
        main_dir = path.realpath(path.join(main_dir, '..', '..'))
        default_filepath = path.join(main_dir, 'default_settings.yml')
        user_filepath = path.join(main_dir, 'settings.yml')
        args = self._get_args()
        if args.settings_path:
            user_filepath = args.settings_path

        # open the default file and get version information
        with open(default_filepath) as default_filestream:
            default_filesettings = yaml.load(default_filestream)

        # FIXME: not used
        current_version = default_filesettings['version'].split('.') # flake8: noqa

        if path.exists(user_filepath):
            filepath = user_filepath
        else:
            filepath = default_filepath

        with open(filepath) as setting_file:
            self.settings = yaml.load(setting_file, _OrderedLoader)

        return SpecialDict(**self.settings)

    def index(self, row, column, parent):
        """Returns QModelIndex to row, column in parent (QModelIndex)"""
        if parent.isValid() and parent.column() != 0:
            return QtCore.QModelIndex()

        if parent.isValid():
            parent_pointer = parent.internalPointer()
            parent_dict = self.root[parent_pointer]
        else:
            parent_dict = self.root
            parent_pointer = ()
        row_key = list(parent_dict.keys())[row]
        child_pointer = (*parent_pointer, row_key)
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

        if index.column() == 0:
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable

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
            if parent_key_list == ((),):
                return QtCore.QModelIndex()
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

        if role != Qt.DisplayRole and role != Qt.EditRole:
            return None

        indexPtr = index.internalPointer()
        if index.column() == 1:    # Column 1, send the value
            return self.root[indexPtr]
        else:                   # Column 0, send the key
            return indexPtr[-1]
