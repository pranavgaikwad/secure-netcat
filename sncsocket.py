# Author : Pranav Gaikwad

import socket

class SncSocket:
    ''' generic class to handle common socket related functions '''
    
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def close(self):
        ''' closes server socket '''
        try:
            self.s.close()
        except:
            raise Exception('Failed closing socket')