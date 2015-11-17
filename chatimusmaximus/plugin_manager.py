from PyQt5 import QtCore
import pluginmanager
import websites


class PluginManager(QtCore.QObject):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.website_interface = pluginmanager.PluginInterface()
        self.website_interface.collect_plugins(websites)
    
    def activate_website(self, website_name: str, *args):
        pass

    def change_website_state(self, website_name: str, state: bool):
        pass
