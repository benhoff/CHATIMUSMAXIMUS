import sys
import asyncio
import logging

import pluginmanager
from PyQt5 import QtWidgets
from quamash import QEventLoop

from zmq.error import ZMQError

from chatimusmaximus.gui import MainWindow
from chatimusmaximus.messaging import ZmqMessaging

log = logging.getLogger()
log.setLevel(logging.INFO)
log.addHandler(logging.StreamHandler())

try:
    import setproctitle
    setproctitle.setproctitle('chatimusmaximus')
except ImportError:
    pass


def main():
    print(__name__)
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
    cmd_line_address = settings_data['display']['address']
    if cmd_line_address:
        messager.publish_to_address(cmd_line_address)

    messager.message_signal.connect(main_window.chat_slot)
    messager.connected_signal.connect(main_window.status_bar.set_widget_status)
    clear = main_window.central_widget.message_area.clear
    messager.clear_signal.connect(clear)
    main_window.command_line_signal.connect(messager.publish_message)

    sockets = settings_data['sockets_to_connect_to']
    cmd_line_address = settings_data['display']['address']

    for socket in sockets:
        if socket:
            try:
                messager.subscribe_to_publisher(socket)
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

    plugin_manager = pluginmanager.PluginInterface()
    plugin_manager.set_entry_points('chatimusmaximus.gui')
    # plugins, names
    plugins, _ = plugin_manager.collect_entry_point_plugins()
    for plug in plugins:
        plug(main_window, messager)

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
    # exit
    sys.exit()


if __name__ == '__main__':
    main()
