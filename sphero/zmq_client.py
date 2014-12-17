import zmq

from .zmq_base import get_address, get_context


ctx = get_context()


class SpheroProxyError(Exception):
    pass


class Proxy:
    def __init__(self, connection_id):
        self.connection_id = connection_id
        self._s = ctx.socket(zmq.REQ)

    def connect(self):
        self._s.connect(get_address(self.connection_id))

    def disconnect(self):
        self._s.disconnect(get_address(self.connection_id))

    def roll(self, speed, heading, state):
        response = self._do_request('roll', speed, heading, state)
        return self._process_simple_response(response)

    def set_rgb(self, r, g, b, save=False):
        response = self._do_request('set_rgb', r, g, b, save)
        return self._process_simple_response(response)

    def set_backlight(self, value):
        response = self._do_request('set_backlight', value)
        return self._process_simple_response(response)

    def ping(self):
        response = self._do_request('ping')
        return self._process_simple_response(response)

    def _ping(self):
        response = self._do_request('_ping')
        if response != '_pong':
            raise SpheroProxyError('Invalid _ping response: %r' % (response,))

    def _do_request(self, cmd, *args):
        self._s.send_json([cmd, args])
        return self._s.recv_json()

    def _process_simple_response(self, response):
        if response != 'ok':
            raise SpheroProxyError('Invalid response: %r' % (response,))
        return None
