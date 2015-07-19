import sys 
from PyQt5 import QtWidgets, QtNetwork, QtCore
from __init__ import get_settings_helper, instantiate_chats_helper
import gui

# create the GUI
app = QtWidgets.QApplication(sys.argv)
main_window = gui.MainWindow()

settings = get_settings_helper()
chat_list = instantiate_chats_helper(settings, main_window)

# connect the sockets signals to the GUI
for chat in chat_list:
    chat.chat_signal.connect(main_window.chat_string_slot)

main_window.show()

# loop... forever
sys.exit(app.exec_())
