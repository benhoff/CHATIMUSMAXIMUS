import sys 
from PyQt5 import QtWidgets, QtNetwork, QtCore

from gui import MainWindow
import socket_protocols

app = QtWidgets.QApplication(sys.argv)

main_window = MainWindow()
main_window.show()
try:
    youtube_socket = socket_protocols.ReadOnlyTCPSocket()
    youtube_socket.chat_signal.connect(main_window.chat_slot)

    # wpc = WatchPeopleCode
    wpc_socket = socket_protocols.ReadOnlyWebSocket(streamer_name='beohoff')
    wpc_socket.chat_signal.connect(main_window.socket_chat_slot)

    irc_client = socket_protocols.ReadOnlyIRCBot('beohoff')
    irc_client.chat_signal.connect(main_window.socket_chat_slot)
except:
    print(sys.exc_info())

sys.exit(app.exec_())
