def _to_list(object):
    if isinstance(object, str):
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
        if children:
            self.children = _to_list(children)
        else:
            self.children = []

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


def _populate_tree(value, parent):
    if isinstance(value, dict):
        for key, val in sorted(value.items()):
            top_level = TreeItem(key, parent)
            parent.appendChild(top_level)
            _populate_tree(val, top_level)
    else:
        parent.item_data.append(value)


class SettingsData(TreeItem):
    def __init__(self, dictionary: dict):
        super().__init__('Settings')
        self.root = self
        _populate_tree(dictionary, self)
