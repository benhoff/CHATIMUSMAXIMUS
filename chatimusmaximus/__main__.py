import sys
import asyncio
import logging

from PyQt5 import QtWidgets
from quamash import QEventLoop
import pluginmanager

from chatimusmaximus.gui import MainWindow
from chatimusmaximus.messaging import ZmqMessaging
from chatimusmaximus.util import create_services_from_settings

log = logging.getLogger()
log.setLevel(logging.INFO)
log.addHandler(logging.StreamHandler())


def main():
    # create the Application
    app = QtWidgets.QApplication(sys.argv)

    # create the event loop and set it in asyncio
    event_loop = QEventLoop(app)
    asyncio.set_event_loop(event_loop)

    # Create the Gui
    main_window = MainWindow()
    settings_data = main_window.settings_model.root
    # Need 3 bits of information from settings. ip addresses, display missing,
    # and general settings

    # Create the recving messaging interface
    messager = ZmqMessaging()
    messager.message_signal.connect(main_window.chat_slot)
    messager.connected_signal.connect(main_window.status_bar.set_widget_status)

    # gather the plugins
    module_manager = pluginmanager.PluginInterface()
    module_manager.set_entry_points('chatimusmaximus.communication_protocols')
    modules = module_manager.collect_entry_point_plugins()

    # need to have the modules in a dict, so get the name and put in dict
    module_dict = {module.__name__.split('.')[-1]: module
                   for module in modules}

    services, addresses = create_services_from_settings(settings_data,
                                                        module_dict)

    messager.subscribe_to_publishers(addresses)
    # show me the money!
    main_window.show()

    # let everything asyncorous run
    try:
        event_loop.run_forever()
    # catch ctrl-C event to allow for graceful closing
    except KeyboardInterrupt:
        pass
    # tell Qt we're going out
    app.deleteLater()
    # close the event loop
    event_loop.close()
    # close the subprocesses
    for service in services:
        service.deactivate()
    # exit
    sys.exit()

if __name__ == '__main__':
    main()
