import sys
import asyncio
import logging

from PyQt5 import QtWidgets
from quamash import QEventLoop
import pluginmanager
from chatimusmaximus.gui import MainWindow
from chatimusmaximus.plugin_wrapper import PluginWrapper
from chatimusmaximus.messaging import ZmqMessaging

log = logging.getLogger()
log.setLevel(logging.INFO)
log.addHandler(logging.StreamHandler())


def _create_services_from_settings(settings, modules: dict):
    _rm_arguments = ['connect', 'display_missing']
    plugin_wrappers = []
    for name, service in settings['services'].items():
        # youtube is special
        if not name == 'youtube':
            module = modules[name]
            for platform, platform_settings in service.items():
                if not platform_settings['connect']:
                    continue
                plugin_wrapper = PluginWrapper(module)
                kwargs = {'--' + key: value for (key, value) in platform_settings.items() if key not in _rm_arguments}
                kwargs['--service_name'] = platform
                plugin_wrapper.activate(invoke_kwargs=kwargs)
                plugin_wrappers.append(plugin_wrapper)
        else:
            # TODO: youtube parsing here
            pass

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

    # Create the recv messaging interface
    messager = ZmqMessaging()
    messager.message_signal.connect(main_window.chat_slot)
    messager.connected_signal.connect(main_window.status_bar.set_widget_status)
    messager.subscribe_to_publishers(settings_data)

    # gather the plugins
    plugin_manager = pluginmanager.PluginInterface()
    plugin_manager.set_entry_points('chatimusmaximus.communication_protocols')
    plugin_manager.collect_entry_point_plugins()

    # collect the modules and turn them into services
    modules = plugin_manager.get_plugins()
    plugins = {module.__name__.split('.')[-1]: module for module in modules}
    services = _create_services_from_settings(settings_data, plugins)

    # show me the money!
    main_window.show()
    try:
        event_loop.run_forever()
    except KeyboardInterrupt:
        pass
    app.deleteLater()
    event_loop.close()
    for service in services:
        service.deactivate()
    sys.exit()

if __name__ == '__main__':
    main()
