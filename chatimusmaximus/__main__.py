import sys 
import asyncio

from PyQt5 import QtWidgets, QtNetwork, QtCore
from quamash import QEventLoop

import gui
from __init__ import get_settings_helper, instantiate_chats_helper

# create the GUI
app = QtWidgets.QApplication(sys.argv)

# create the event loop
event_loop = QEventLoop(app)
asyncio.set_event_loop(event_loop)

main_window = gui.MainWindow()

settings = get_settings_helper()
chat_list = instantiate_chats_helper(settings, main_window, event_loop)

# connect the sockets signals to the GUI
for chat in chat_list:
    chat.chat_signal.connect(main_window.chat_string_slot)

main_window.show()
with event_loop:
    event_loop.run_forever()
