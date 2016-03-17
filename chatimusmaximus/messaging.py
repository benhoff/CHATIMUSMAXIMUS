from PyQt5 import QtCore
import zmq
from threading import Thread


class ZmqMessaging(QtCore.QObject):
    message_signal = QtCore.pyqtSignal(str, str, str)
    connected_signal = QtCore.pyqtSignal(bool, str)

    def __init__(self, parent=None):
        super().__init__(parent)
        context = zmq.Context()
        self.sub_socket = context.socket(zmq.SUB)
        self.sub_socket.setsockopt(zmq.SUBSCRIBE, b'')
        self.thread = Thread(target=self.recv_sub_socket, daemon=True)
        self.thread.start()

    def subscribe_to_publishers(self, settings: dict):
        for services, values in settings['services'].items():
            if not services == 'youtube':
                for platform_values in values.values():
                    if platform_values['connect']:
                        self.sub_socket.connect(platform_values['socket_address'])
            else:
                # youtube is special
                pass

    def recv_sub_socket(self):
        while True:
            frame = self.sub_socket.recv_multipart()
            frame = [x.decode('ascii') for x in frame]
            frame_length = len(frame)
            if frame_length == 4:
                del frame[1]
                self.message_signal.emit(*frame)
            elif frame_length == 2:
                state = frame[1]
                if state == 'CONNECTED':
                    state = True
                else:
                    state = False
                self.connected_signal.emit(state, frame[0])
