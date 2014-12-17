from .zmq_client import Proxy


class Sphero:
    def __init__(self, sphero_id):
        self.sphero_id = sphero_id
        self._proxy = None

    def connect(self, sphero_id=None):
        if sphero_id is None:
            sphero_id = self.sphero_id
        self._proxy = Proxy(sphero_id)
        self._proxy.connect()

    def disconnect(self):
        self._proxy.disconnect()
        self._proxy = None

    def roll(self, speed, heading, state=1):
        return self._proxy.roll(speed, heading, state)

    def set_rgb(self, r, g, b, save=False):
        return self._proxy.set_rgb(r, g, b, save)

    def set_backlight(self, value):
        return self._proxy.set_backlight(value)

    def ping(self):
        return self._proxy.ping()
