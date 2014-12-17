import zmq


BASE_ADDR = 'ipc:///tmp/sphero_zmq-%s.sock'

ctx = zmq.Context()


def get_context():
    # global ctx
    # if ctx is None:
    #     ctx = zmq.Context()

    return ctx


def get_address(conn_id):
    return BASE_ADDR % (conn_id,)
