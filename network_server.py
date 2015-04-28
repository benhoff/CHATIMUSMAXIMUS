from PyQt5 import QtNetwork, QtCore

class SocketThread(QtCore.QThread):
    error = QtCore.pyqtSignal(QtNetwork.QTcpSocket.SocketError)
    # TODO: Connect readData to a signal which emits the data
    def __init__(self, id, parent=None):
        super(SocketThread, self).__init__(parent)
        self.socket_descriptor = id
        self.socket = None

    def run(self):
        print(self.socket_descriptor, " Starting Thread")
        self.socket = QtNetwork.QTcpSocket()
        if not self.socket.setSocketDescriptor(self.socket_descriptor):
            self.error.emit(self.socket.error())
            return
        
        # Think the slot is called directly, might be source of bugs later. CHECK
        self.socket.readyRead.connect(self.readyRead)
        self.socket.disconnected.connect(self.disconnected)

        print(self.socket_descriptor, " Client connected")

        # make this thread a loop
        self.exec_()

    @QtCore.pyqtSlot() 
    def readyRead(self):
        data = self.socket.readAll()
        print(self.socket_descriptor, " Data in: ", data)

        self.socket.write(data)

    @QtCore.pyqtSlot()
    def disconnected(self):
        print(self.socket_descriptor, " Disconnected")
        self.socket.deleteLater()
        self.exit(0)

class NetworkServer(QtNetwork.QTcpServer):
    # TODO: Pass into own thread and call in a exec loop
    def __init__(self, parent=None):
        super(NetworkServer, self).__init__(parent)
        self.listen(port=1024)
   
    def incomingConnection(self, socket_desciptor):
        print(socket_desciptor, " Connecting...")
        # TODO: Think about this memory management piece
        thread = SocketThread(socket_desciptor, self)
        thread.finished.connect(thread.deleteLater)
        thread.start()

    @QtCore.pyqtSlot()
    def start_read(self):
        pass
