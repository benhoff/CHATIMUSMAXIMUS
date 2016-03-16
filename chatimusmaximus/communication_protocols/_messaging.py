import asyncio

import zmq
import zmq.asyncio


class ZmqMessaging:
    def __init__(self, service_name, pub_port):
        self._service_name = service_name.encode('ascii')
        self.start_messaging(pub_port)

    def start_messaging(self, pub_port):
        context = zmq.Context()
        self.pub_socket = context.socket(zmq.PUB)
        self.pub_socket.bind(pub_port)

    def send_message(self, *msg):
        msg = [x.encode('ascii') for x in msg]
        msg.insert(0, self._service_name)
        self.pub_socket.send_multipart(msg)
