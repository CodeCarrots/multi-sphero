import zmq
import logging

from zmq_base import get_address, get_context


ctx = get_context()


def run_server(conn_id, sphero):
    s = ctx.socket(zmq.REP)
    s.bind(get_address(conn_id))

    def ping():
        sphero.ping()

    handlers = {
        'roll': sphero.roll,
        'set_rgb': sphero.set_rgb,
        'set_backlight': sphero.set_backlight,
        'ping': ping,

        '_ping': (lambda: '_pong'),
    }

    while True:
        logging.debug('Receiving message...')
        try:
            msg = s.recv_json()
        except KeyboardInterrupt:
            break

        logging.debug('Got: %r', msg)

        if not isinstance(msg, (list, tuple)) or len(msg) != 2:
            logging.error('Invalid msg received: %r', msg)
            s.send_json('invalid')
            continue

        cmd, args = msg

        handler = handlers.get(cmd, None)
        if not handler:
            logging.error('Unknown cmd received: %r', msg)
            s.send_json('not found')
            continue

        try:
            ret = handler(*args)
        except Exception as e:
            logging.exception(e)
            s.send_json('crashed')
            continue

        if isinstance(ret, str):
            s.send_json(ret)
        elif ret is None:
            s.send_json('ok')
        else:
            logging.error('Invalid handler response type: %r', ret)
            s.send_json('error')

    s.close()


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('connection_id', help='Proxy socket connection ID')
    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG)

    class DummySphero:
        def roll(self, speed, heading, state=1):
            logging.info('DummySphero: roll: %r', (speed, heading, state))

        def set_rgb(self, r, g, b, save=False):
            logging.info('DummySphero: set_rgb: %r', (r, g, b, save))

        def set_backlight(self, value):
            logging.info('DummySphero: set_backlight: %r', (value,))

    s = DummySphero()

    run_server(args.connection_id, s)
