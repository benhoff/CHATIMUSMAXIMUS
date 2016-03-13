import sys
import asyncio
import logging

from PyQt5 import QtWidgets
from quamash import QEventLoop
import pluginmanager
from chatimusmaximus.gui import MainWindow
from chatimusmaximus.messaging import ZmqMessaging

log = logging.getLogger()
log.setLevel(logging.INFO)
log.addHandler(logging.StreamHandler())


def main():
    # create the Application
    app = QtWidgets.QApplication(sys.argv)

    # create the event loop
    event_loop = QEventLoop(app)
    asyncio.set_event_loop(event_loop)

    # Create the Gui
    main_window = MainWindow()
    settings_data = main_window.settings_model.root

    # Create the messaging interface
    # messager = ZmqMessaging()
    # messager.message_signal.connect(main_window.chat_slot)

    plugin_manager = pluginmanager.PluginInterface()
    plugin_manager.set_entry_points('chatimusmaximus.communication_protocols')
    plugin_manager.collect_entry_point_plugins()

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
