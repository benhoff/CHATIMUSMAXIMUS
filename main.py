import sys 
from PyQt5 import QtWidgets, QtNetwork, QtCore
from main_window import MainWindow
from network_server import NetworkServer

app = QtWidgets.QApplication(sys.argv)

main_window = MainWindow()
main_window.show()

network_server = NetworkServer()
test_socket = QtNetwork.QTcpSocket()

test_socket.connectToHost('127.0.0.1', 1024)
print("Sending data!")
test_socket.write(QtCore.QByteArray("Testing testing!"))


sys.exit(app.exec_())
