import sys
import asyncio

from PyQt5 import QtWidgets
from quamash import QEventLoop
import pluginmanager
# TODO: Change to `listener-plugins`
import plugins

from gui import MainWindow
import logging
log = logging.getLogger()
log.setLevel(logging.INFO)
log.addHandler(logging.StreamHandler())
from __init__ import get_settings_helper, instantiate_plugin_manager


def main():
    # create the GUI
    app = QtWidgets.QApplication(sys.argv)

    # create the event loop
    event_loop = QEventLoop(app)
    asyncio.set_event_loop(event_loop)

    main_window = MainWindow()

    # need chat_slot to be able to add to add the chat signal
    chat_slot = main_window.central_widget.message_area.chat_slot

    settings = get_settings_helper()
    # this methods also handles passing in values to websites
    plugin_manager = instantiate_plugin_manager(settings)
    main_window.set_settings(settings)
    chat_list = plugin_manager.get_instances()

    # connect the sockets signals to the GUI
    for chat in chat_list:
        chat.chat_signal.connect(chat_slot)
        chat.connected_signal.connect(main_window.status_bar.set_widget_status)

    listener_interface = pluginmanager.PluginInterface()
    listener_interface.collect_plugins(plugins)

    listener_list = listener_interface.get_instances()
    #main_window.central_widget.message_area.listeners = listener_list

    main_window.show()
    try:
        event_loop.run_forever()
    except KeyboardInterrupt:
        pass
    for chat in chat_list:
        if chat.process:
            chat.process.terminate()
    event_loop.close()
    sys.exit()

if __name__ == '__main__':
    main()
