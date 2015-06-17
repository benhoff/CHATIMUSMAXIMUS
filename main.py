import sys 
from PyQt5 import QtWidgets, QtNetwork, QtCore
from gui import MainWindow

# import a couple of the instances from the __init__ file
from . import youtube_socket, wpc_socket, irc_client

app = QtWidgets.QApplication(sys.argv)

main_window = MainWindow()
main_window.show()

youtube_socket.chat_signal.connect(main_window.chat_slot)
wpc_socket.chat_signal.connect(main_window.socket_chat_slot)
irc_client.chat_signal.connect(main_window.socket_chat_slot)

sys.exit(app.exec_())
