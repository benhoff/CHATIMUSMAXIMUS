import sys
import asyncio
import logging

from PyQt5 import QtWidgets
from quamash import QEventLoop
import pluginmanager
from chatimusmaximus.gui import MainWindow
from chatimusmaximus.plugin_wrapper import PluginWrapper

log = logging.getLogger()
log.setLevel(logging.INFO)
log.addHandler(logging.StreamHandler())


def _really_cool_function(settings, modules: dict):
    plugin_wrappers = []
    for name, service in settings['services'].items():
        # youtube is special
        if not name == 'youtube':
            module = modules[name]
            for platform, platform_settings in service.items():
                plugin_wrapper = PluginWrapper(module)
                # FIXME
                plugin_wrapper.activate([value for (key, value) in platform_settings.items() if key not in ['connect', 'display_missing']])

                plugin_wrappers.append(plugin_wrapper)

    return plugin_wrappers


def main():
    # create the Application
    app = QtWidgets.QApplication(sys.argv)

    # create the event loop
    event_loop = QEventLoop(app)
    asyncio.set_event_loop(event_loop)

    # Create the Gui
    main_window = MainWindow()
    settings_data = main_window.settings_model.root

    plugin_manager = pluginmanager.PluginInterface()
    plugin_manager.set_entry_points('chatimusmaximus.communication_protocols')
    plugin_manager.collect_entry_point_plugins()

    modules = plugin_manager.get_plugins()
    plugins = {module.__name__.split('.')[-1]: module for module in modules}
    _really_cool_function(settings_data, plugins)

    # Create the messaging interface
    # messager = ZmqMessaging()
    # messager.message_signal.connect(main_window.chat_slot)


    main_window.show()
    try:
        event_loop.run_forever()
    except KeyboardInterrupt:
        pass
    app.deleteLater()
    plugin_manager.terminate_plugins()
    event_loop.close()
    sys.exit()

if __name__ == '__main__':
    main()
