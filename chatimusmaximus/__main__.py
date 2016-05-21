import sys
import asyncio
import logging
import atexit

from PyQt5 import QtWidgets
from quamash import QEventLoop
import pluginmanager

from zmq.error import ZMQError

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

    # Create the recving messaging interface
    messager = ZmqMessaging()
    messager.message_signal.connect(main_window.chat_slot)
    messager.connected_signal.connect(main_window.status_bar.set_widget_status)
    main_window.command_line_signal.connect(messager.publish_message)

    # gather the plugins
    module_manager = pluginmanager.PluginInterface()
    module_manager.set_entry_points('chatimusmaximus.communication_protocols')
    modules, names = module_manager.collect_entry_point_plugins()

    # need to have the modules in a dict, so get the name and put in dict
    module_dict = {module.__name__.split('.')[-1]: module
                   for module in modules}

    services, addresses = create_services_from_settings(settings_data,
                                                        module_dict)

    atexit.register(_destroy_services, services)

    sockets = settings_data['sockets_to_connect_to']
    cmd_line_address = settings_data['display']['address']

    for socket in sockets:
        try:
            messager.subscribe_to_publishers(socket)
        except ZMQError:
            # TODO: change to a logging command
            s = 'socket address to connect to {} is throwing errors!'
            print(s.format(socket))

    try:
        if cmd_line_address:
            messager.publish_to_address(cmd_line_address)
    except ZMQError:
        s = 'command line address to connect to {} is throwing errors!'
        print(s.format(cmd_line_address))

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


def _destroy_services(services):
    for service in services:
        service.deactivate()

if __name__ == '__main__':
    main()
