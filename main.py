import sys 
from PyQt5 import QtWidgets, QtNetwork, QtCore
from main_window import MainWindow
from network_server import NetworkServer

app = QtWidgets.QApplication(sys.argv)

main_window = MainWindow()
main_window.show()

network_server = NetworkServer()
network_server.chat_signal.connect(main_window.chat_slot)
"""
test_socket = QtNetwork.QTcpSocket(network_server)

test_socket.connectToHost('127.0.0.1', 54545)
print("Sending data!")
test_socket.write(QtCore.QByteArray("Testing testing!"))
"""
sys.exit(app.exec_())
