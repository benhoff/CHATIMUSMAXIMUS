import sys 
from PyQt5 import QtWidgets, QtNetwork, QtCore
from main_window import MainWindow
from network_server import NetworkServer
from socket_client import SocketThread
app = QtWidgets.QApplication(sys.argv)

main_window = MainWindow()
main_window.show()

network_server = NetworkServer()
network_server.chat_signal.connect(main_window.chat_slot)

# wpc = WatchPeopleCode
wpc_socket = SocketThread(streamer_name='beohoff')
wpc_socket.chat_signal.connect(main_window.socket_chat_slot)
wpc_socket.start()

sys.exit(app.exec_())
