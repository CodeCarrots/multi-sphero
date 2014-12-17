from sphero_base import init_sphero
from sphero.zmq_server import run_server

if __name__ == '__main__':
    import argparse
    import logging

    parser = argparse.ArgumentParser()
    parser.add_argument('address', help='Sphero Bluetooth address')
    parser.add_argument('connection_id', help='Proxy socket connection ID')
    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG)

    s = init_sphero(args.address)

    run_server(args.connection_id, s)

    s.disconnect()
