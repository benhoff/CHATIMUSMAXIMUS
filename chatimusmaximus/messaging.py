import time
from threading import Thread

import zmq
from PyQt5 import QtCore
from vexmessage import create_vex_message, decode_vex_message


class ZmqMessaging(QtCore.QObject):
    # source, sender, message
    message_signal = QtCore.pyqtSignal(str, str, str)
    connected_signal = QtCore.pyqtSignal(bool, str)

    def __init__(self, parent=None):
        super().__init__(parent)
        context = zmq.Context()
        self.sub_socket = context.socket(zmq.SUB)
        self.sub_socket.setsockopt(zmq.SUBSCRIBE, b'')
        self.pub_socket = context.socket(zmq.PUB)
        self.thread = Thread(target=self._recv_sub_socket, daemon=True)
        self.thread.start()
        # service, user, msg, time
        self._last_message = ('', '', '', time.time())

    @QtCore.pyqtSlot(str, str, str)
    def publish_message(self, service, user, text, target=''):
        # FIXME
        frame = create_vex_message(target,
                                   service,
                                   'MSG',
                                   (user,
                                    text))

        self.pub_socket.send_multipart(frame)

    def send_command(self, text, target=''):
        # FIXME
        frame = create_vex_message(target,
                                   'chatimus',
                                   'CMD',
                                   (text,))

        self.pub_socket.send_multipart(frame)

    def subscribe_to_publisher(self, address: str):
        self.sub_socket.connect(address)

    def publish_to_address(self, address: str):
        self.pub_socket.connect(address)

    def _recv_sub_socket(self):
        while True:
            frame = self.sub_socket.recv_multipart()
            msg = decode_vex_message(frame)
            if msg.type == 'MSG':
                if not self._duplicate_message(msg):
                    self.message_signal.emit(msg.source,
                                             msg.contents[0],
                                             msg.contents[1])

            elif msg.type == 'STATUS':
                state = msg.contents[0]
                if state == 'CONNECTED':
                    state = True
                elif state == 'DISCONNECTED':
                    state = False
                else:
                    continue
                self.connected_signal.emit(state, msg.source)

    def _duplicate_message(self, message):
        """
        zmq is giving me grief. Tiny method
        to prevent duplicate messages from
        being displayed
        """
        last_message = self._last_message
        # source, user, msg, time
        self._last_message = (message.source,
                              message.contents[0],
                              message.contents[1],
                              time.time())

        last_user = last_message[1]
        if last_user != self._last_message[1]:
            return False

        if (last_message[2] == self._last_message[2] and
                self._last_message[3] - last_message[3] < 1):
            return True

        return False
