from PyQt5 import QtCore
import zmq
from threading import Thread
import time


class ZmqMessaging(QtCore.QObject):
    message_signal = QtCore.pyqtSignal(str, str, str)
    connected_signal = QtCore.pyqtSignal(bool, str)

    def __init__(self, parent=None):
        super().__init__(parent)
        context = zmq.Context()
        self.sub_socket = context.socket(zmq.SUB)
        self.sub_socket.setsockopt(zmq.SUBSCRIBE, b'')
        self.pub_socket = context.socket(zmq.PUB)
        self.thread = Thread(target=self.recv_sub_socket, daemon=True)
        self.thread.start()
        # service, user, msg, time
        self._last_message = ['', '', '', time.time()]

    def subscribe_to_publisher(self, address: str):
        self.sub_socket.connect(address)

    def publish_to_address(self, address):
        self.pub_socket.connect(address)

    @QtCore.pyqtSlot(str, str, str)
    def publish_message(self, service, user, text):
        frame = [service, 'MSG', user, text]
        self.pub_socket.send_pyobj(frame)

    def _duplicate_message(self, message):
        """
        zmq is giving me grief. Tiny method
        to prevent duplicate messages from
        being displayed
        """
        last_message = self._last_message
        self._last_message = list(message)
        self._last_message.append(time.time())
        last_user = last_message[1]
        if last_user != message[1]:
            return False

        if (last_message[2] == message[2] and
                self._last_message[3] - last_message[3] < 1):
            return True

        return False

    def recv_sub_socket(self):
        while True:
            frame = self.sub_socket.recv_pyobj()
            frame_length = len(frame)
            if frame_length == 4:
                del frame[1]
                if not self._duplicate_message(frame):
                    self.message_signal.emit(*frame)
            elif frame_length == 2:
                state = frame[1]
                if state == 'CONNECTED':
                    state = True
                else:
                    state = False
                self.connected_signal.emit(state, frame[0])
