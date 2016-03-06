import sys
import asyncio

from PyQt5 import QtWidgets
from quamash import QEventLoop
import pluginmanager

from gui import MainWindow
from plugin_manager import PluginManager
from settings_manager import SettingsManager
import logging
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
    # plugins to include different websites (and listeners?)
    plugin_manager = PluginManager()
    plugin_manager.register_main_window(main_window)

    # User Settings
    settings_manager = SettingsManager()
    settings_manager.register_main_window(main_window)
    settings_manager.register_plugin_manager(plugin_manager)

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
