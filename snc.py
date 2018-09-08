# Author: Pranav Gaikwad

import sys
import argparse

from sncclient import SncSocketClient
from sncserver import SncSocketServer

# custom usage message
USAGE_MSG = 'usage: snc.py [-h] [-l] --key KEY server port'

# parses CLI arguments
argparser = argparse.ArgumentParser(usage=USAGE_MSG)
# positional arguments
# Refer https://docs.python.org/2/library/argparse.html#nargs for nargs argument
argparser.add_argument("connection", nargs='*', help="Connection string in format [server] [port]")
# other args
argparser.add_argument("-l", help="Listen mode", action="store_true", default=False)
argparser.add_argument("--key", help="Encryption key", required=True)

args = argparser.parse_args()

# 'connection' argument is a list of all arguments remained after parsing --key & -l
# it could be server & port values; or just a port value when '-l' is set
connection_string_list = args.connection

# checks if '-l' argument is set. 
# if yes, program will run in 'LISTEN' mode
LISTEN = args.l 

HOST = ''
PORT = ''

# if 'listen' mode is set, connection_string_list only has PORT
# in it. If not, connection_string_list needs to be parsed
# as SERVER & PORT. this is due to limitation of 'argparser'
# module which does not support conditional positional variables
if LISTEN:
    try:
        PORT = int(connection_string_list[0])
    except IndexError:
        print 'Please specify a port'
        sys.exit(1)
else:
    try:
        HOST = connection_string_list[0]
        PORT = int(connection_string_list[1])
    except IndexError:
        print 'Please specify connection string in [server] [port] format'
        sys.exit(1)

# client socket
client = SncSocketClient()

# server socket
server = SncSocketServer()

# server routine
if LISTEN:
    try: 
        # start the server
        conn, addr = server.start(PORT)
        while True:
            data = conn.recv(SncSocketServer.MAX_BUFFER_SIZE)
            if not data:
                break
            print data
    except KeyboardInterrupt:
        conn.close()
        server.close()
# client routine
else:
    try:
        client.connect(HOST, PORT)
        while True:
            data = raw_input('')
            client.send(data)
    except KeyboardInterrupt:
        client.close()