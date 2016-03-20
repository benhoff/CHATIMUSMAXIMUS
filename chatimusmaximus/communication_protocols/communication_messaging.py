import asyncio

import zmq


class ZmqMessaging:
    def __init__(self, service_name, pub_port):
        self._service_name = service_name
        self.start_messaging(pub_port)

    def start_messaging(self, pub_port):
        context = zmq.Context()
        self.pub_socket = context.socket(zmq.PUB)
        try:
            self.pub_socket.bind(pub_port)
        except zmq.error.ZMQError:
            print('Incorrect value passed in for socket address in {}, fix it in your settings/default_settings.yml'.format(self._service_name))

    def send_message(self, *msg):
        msg = list(msg)
        msg.insert(0, self._service_name)
        self.pub_socket.send_pyobj(msg)
