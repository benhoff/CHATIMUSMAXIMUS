from PyQt5 import QtCore
import pluginmanager
from pluginmanager import module_filters

import websites
from websites.website_plugin import WebsitePlugin

def _filter_website(platform_name, websites):
    for website in websites:
        if websites.platfrom == platform_name:
            return website
    return None

class PluginManager(QtCore.QObject):
    def __init__(self, parent=None):
        super().__init__(parent)
        # create the website plugin manager
        self.website_plugins = pluginmanager.PluginInterface()
        # website plugins only `WebsitePlugin` class
        subclass_filter = module_filters.SubclassParser(WebsitePlugin)
        self.website_plugins.module_manager.set_module_filters(subclass_filter)

        self.website_plugins.collect_plugins(websites)

    def _get_website(self, website_name):
        website_filter = lambda x: _filter_website(website_name, x)
        return self.website_plugins.get_instances(website_filter)
    
    def activate_website(self, website_name: str, *args):
        website = self._get_website(website_name)
        website.activate(*args)

    def change_website_state(self, website_name: str, state: bool):
        website = self._get_website(website_name)
        if state:
            website.activate()
        else:
            website.deactivate()

    def register_main_window(self, main_window):
        websites = self.website_plugins.get_instances()
        for website in websites:
            website.chat_signal.connect(main_winow.chat_slot)

    def terminate_plugins(self):
        for chat in self.website_plugins.get_instances():
            if chat.process:
                chat.process.terminate()
