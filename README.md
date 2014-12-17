multi-sphero
============

Helper code for Sphero demo at GGC CC


Requirements
------------

Python 3.x (tested with 3.4):

      $ pip install -r requirements.txt


Running
-------

First, you should probably install this module (although it's
perfectly possible to run without installing if you set PYTHONPATH
appropriately):

      $ python ./setup.py install

For each Sphero device run connection/handler/multiplexer server:

      $ python ./sphero/server.py fe:dc:ba:98:76:54 BRO

where `fe:dc:ba:98:76:54` is the address of your Sphero and `BRO` is
some arbitrary identifier (unique for each device, though).

Once the server has established connection with your Sphero device,
you can use the "client" part of this module:

```python
from sphero import Sphero
s = Sphero('BRO')
s.connect()
s.set_rgb(0, 255, 0)
s.roll(0, 180)
s.disconnect()
```

Note: the `BRO` identifier is the same used in the server invocation.

Client code has to be run on the same machine as the server but
multiple client processes can access the same Sphero device. Perfect
for running the client code from multiple IPython notebooks. Plus,
most of the time it's enough to just restart the multiplexer server if
it loses its connection to Sphero, without affecting interactive
client sessions (ØMQ magic FTW!).
