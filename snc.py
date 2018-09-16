#!/usr/bin/env python

'''
Author   : Pranav Gaikwad
Unity Id : 200203543
'''


from sncclient import SncSocketClient
from sncserver import SncSocketServer
from sncargparser import parse_snc_args

# parse arguments
HOST, PORT, LISTEN, KEY = parse_snc_args()

# client socket
client = SncSocketClient()

# server socket
server = SncSocketServer()

# server routine
if LISTEN:
    server.start(PORT, KEY)
# client routine
else:
    client.start(HOST, PORT, KEY)
