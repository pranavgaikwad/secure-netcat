# Author : Pranav Gaikwad
import sys
import argparse

def parse_snc_args():
    # custom usage message
    USAGE_MSG = 'snc.py [-h] [-l] --key KEY server port'
    
    # parses CLI arguments
    argparser = argparse.ArgumentParser(usage=USAGE_MSG)
    # positional arguments
    # Refer https://docs.python.org/2/library/argparse.html#nargs for nargs argument
    argparser.add_argument("connection", nargs='*', help="Connection string in format [server] [port]")
    # other args
    argparser.add_argument("-l", help="listen mode / start as client", action="store_true", default=False)
    argparser.add_argument("--key", help="encryption key", required=True)
    
    args = argparser.parse_args()
    
    # 'connection' argument is a list of all arguments remained after parsing --key & -l
    # it could be server & port values; or just a port value when '-l' is set
    connection_string_list = args.connection
    
    # checks if '-l' argument is set. 
    # if yes, program will run in 'LISTEN' mode
    LISTEN = args.l 
    
    HOST = ''
    PORT = ''
    KEY = args.key

    if len(KEY) < 16:
        sys.stderr.write('Key should be 16 characters long\n')
        sys.exit(1)
    
    # if 'listen' mode is set, connection_string_list only has PORT
    # in it. If not, connection_string_list needs to be parsed
    # as SERVER & PORT. this is due to limitation of 'argparser'
    # module which does not support conditional positional variables
    if LISTEN:
        try:
            PORT = int(connection_string_list[0])
        except IndexError:
            sys.stderr.write('Please specify a port\n')
            sys.exit(1)
    else:
        try:
            HOST = connection_string_list[0]
            PORT = int(connection_string_list[1])
        except IndexError:
            sys.stderr.write('Please specify connection string in [server] [port] format\n')
            sys.exit(1)
        except ValueError:
            sys.stderr.write('Incorrect host or port\n')
            sys.exit(1)

    return HOST, PORT, LISTEN, KEY