import sys 
from PyQt5 import QtWidgets, QtNetwork, QtCore
from main_window import MainWindow
from network_server import NetworkServer
from socket_client import Socket
from irc_client import ReadOnlyIRCBot

app = QtWidgets.QApplication(sys.argv)

main_window = MainWindow()
main_window.show()

network_server = NetworkServer()
network_server.chat_signal.connect(main_window.chat_slot)

# wpc = WatchPeopleCode
wpc_socket = Socket(streamer_name='beohoff')
wpc_socket.chat_signal.connect(main_window.socket_chat_slot)

irc_client = ReadOnlyIRCBot('beohoff')
irc_client.chat_signal.connect(main_window.socket_chat_slot)

sys.exit(app.exec_())
