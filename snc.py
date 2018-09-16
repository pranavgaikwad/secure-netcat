#!/usr/bin/env python

'''
Author   : Pranav Gaikwad
Unity Id : 200203543
'''


from sncclient import SncSocketClient
from sncserver import SncSocketServer
from sncargparser import parse_snc_args

if __name__ == "__main__":
    # parse arguments
    HOST, PORT, LISTEN, KEY = parse_snc_args()

    # server routine
    if LISTEN:
        SncSocketServer().start(PORT, KEY)
    # client routine
    else:
        SncSocketClient().start(HOST, PORT, KEY)
