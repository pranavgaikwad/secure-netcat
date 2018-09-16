'''
Author   : Pranav Gaikwad
Unity Id : 200203543
'''

import sys
import argparse

from sncaeshelper import AesHelper


def parse_snc_args():
    """
    parses command line arguments
    """
    # custom usage message
    usage_msg = 'snc.py [-h] [-l] --key KEY server port'

    # parses CLI arguments
    argparser = argparse.ArgumentParser(usage=usage_msg)
    # positional arguments
    # Refer https://docs.python.org/2/library/argparse.html#nargs
    argparser.add_argument("connection", nargs='*',
                           help="Connection string in format [server] [port]")
    # other args
    argparser.add_argument(
        "-l", help="listen mode / start as client",
        action="store_true", default=False)
    argparser.add_argument("--key", help="encryption key", required=True)

    args = argparser.parse_args()

    # 'connection' argument is a list of all
    # arguments remained after parsing --key & -l
    # it could be server & port values; or just a
    # port value when '-l' is set
    connection_string_list = args.connection

    # checks if '-l' argument is set.
    # if yes, program will run in 'listen' mode
    listen = args.l

    host = ''
    port = ''
    key = args.key

    if len(key) < AesHelper.LENGTH_IDEAL_KEY:
        sys.stderr.write('Key should be at least %s characters long\n' %
                         str(AesHelper.LENGTH_IDEAL_KEY))
        sys.exit(1)

    # if 'listen' mode is set, connection_string_list only has PORT
    # in it. If not, connection_string_list needs to be parsed
    # as SERVER & port. this is due to limitation of 'argparser'
    # module which does not support conditional positional variables
    if listen:
        try:
            port = int(connection_string_list[0])
        except IndexError:
            sys.stderr.write('Please specify a port\n')
            sys.exit(1)
    else:
        try:
            host = connection_string_list[0]
            port = int(connection_string_list[1])
        except IndexError:
            sys.stderr.write(
                'Please specify connection string in [server] [port] format\n')
            sys.exit(1)
        except ValueError:
            sys.stderr.write('Incorrect host or port\n')
            sys.exit(1)

    return host, port, listen, key
