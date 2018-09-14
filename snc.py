# Author : Pranav Gaikwad

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


'''
    # this is sample one way communication code
    # ignore this code 

    conn, addr = server.start(PORT)
    while True:
        try: 
            data = conn.recv(SncSocketServer.MAX_BUFFER_SIZE)
            if not data:
                break
            print data
        except (KeyboardInterrupt, EOFError):
            conn.close()
            server.close()
            break

    client.connect(HOST, PORT)
    while True:
        try: 
            data = raw_input('')
            client.send(data)
        except (KeyboardInterrupt, EOFError):
            client.close()
            break

'''