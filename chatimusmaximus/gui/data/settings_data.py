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
        for key, val in value.items():
            top_level = TreeItem(key, parent)
            child = _return_tree(value, top_level)
            top_level.appendChild(child)
            return top_level
    else:
        return TreeItem(value, parent)


class SettingsData(TreeItem):
    def __init__(self, dictionary: dict):
        super().__init__(None)
        self.root = self
        self.data = 'Settings'
        self.appendChild(_return_tree(dictionary, self))
