from PyQt5 import QtNetwork, QtCore

class SocketThread(QtCore.QThread):
    error = QtCore.pyqtSignal(QtNetwork.QTcpSocket.SocketError)
    chat_signal = QtCore.pyqtSignal(QtCore.QByteArray)

    # TODO: Connect readData to a signal which emits the data
    def __init__(self, id, parent=None):
        super(SocketThread, self).__init__(parent)
        self.socket_descriptor = id
        self.socket = None

    def run(self):
        self.socket = QtNetwork.QTcpSocket(parent=self)
        if not self.socket.setSocketDescriptor(self.socket_descriptor):
            self.error.emit(self.socket.error())
            return
        
        # Think the slot is called directly, might be source of bugs later. CHECK
        self.socket.readyRead.connect(self.readyRead)
        self.socket.disconnected.connect(self.disconnected)

        # make this thread a loop
        self.exec_()

    @QtCore.pyqtSlot() 
    def readyRead(self):
        data = self.socket.readAll()
        self.chat_signal.emit(data)

    @QtCore.pyqtSlot()
    def disconnected(self):
        self.socket.deleteLater()
        self.exit(0)

class NetworkServer(QtNetwork.QTcpServer):
    chat_signal = QtCore.pyqtSignal(QtCore.QByteArray)
    # TODO: Pass into own thread and call in a exec loop
    def __init__(self, parent=None):
        super(NetworkServer, self).__init__(parent)
        self.listen(port=54545)
        self.sockets = []
   
    def incomingConnection(self, socket_desciptor):
        # TODO: Think about this memory management piece
        print("incoming connection")
        thread = SocketThread(socket_desciptor)
        thread.finished.connect(thread.deleteLater)
        thread.chat_signal.connect(self.chat_slot)
        thread.start()
        self.sockets.append(thread)
    
    @QtCore.pyqtSlot(QtCore.QByteArray)
    def chat_slot(self, qbyte_array):
        self.chat_signal.emit(qbyte_array)
