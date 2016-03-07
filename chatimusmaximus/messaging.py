import asyncio
from PyQt5 import QtCore
import zmq
import zmq.asyncio


class ZmqMessaging(QtCore.QObject):
    message_signal = QtCore.pyqtSignal(str, str, str)

    def __init__(self, parent=None):
        super().__init__(parent)
        context = zmq.asyncio.Context()
        self.sub_socket = context.socket(zmq.SUB)
        self.sub_socket.setsockopt(zmq.SUBSCRIBE, b'')

        self.control_socket = context.socket(zmq.REP)
        self.control_socket.bind('tcp://127.0.0.1:5986')
        event_loop = asyncio.get_event_loop()
        event_loop.call_soon(self.recv_control_socket)
        event_loop.call_soon(self.recv_sub_socket)

    async def recv_control_socket(self):
        while True:
            frame = await self.control_socket.recv_multipart()
            # response socket MUST send response
            self.control_socket.send(b'')
            # bind the sent socket to the 
            self.sub_socket.bind(frame.decode('ascii'))

    async def recv_sub_socket(self):
        while True:
            frame = await self.sub_socket.recv_multipart()
            frame = (x.decode('ascii') for x in frame)
            self.msg_signal.emit(*frame)
