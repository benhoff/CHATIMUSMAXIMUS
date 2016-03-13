import sys
import subprocess


class BaseCommunicationProto:
    """
    subclass this so you don't have to think about how to activate
    a subprocess. Or don't. But I'm not, not going to.
    """
    def __init__(self):
        self._subprocess = None
        self._save_args = None
        self._service_name = None
        self.pub_socket = None

    def activate(self, invoke_args, invoke_kwargs, *args, **kwargs):
        activate_args = (sys.executable,
                         __file__,
                         *invoke_args,
                         **invoke_kwargs)

        self._save_args = (invoke_args, invoke_kwargs, args, kwargs)

        self._subprocess = subprocess.Popen(activate_args, *args, **kwargs)

    def deactivate(self):
        # TODO: do terminate instead of kill, and schedule a callback to make
        # sure the process is terminated. Then kill
        self._subprocess.kill()

    def restart(self):
        self.deactivate()
        self.activate(*self._save_args)

    def start_messaging(self, service_name)
        self._service_name = service_name.encode('ascii')
        context = zmq.Context()
        self.pub_socket = context.socket(zmq.PUB)
        self.pub_socket.bind(pub_address)

    def send_message(self, *msg):
        msg = (x.encode('ascii') for x in msg)
        self.pub_socket.send_multipart(msg)
