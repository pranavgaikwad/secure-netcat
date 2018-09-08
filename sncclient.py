# Author : Pranav Gaikwad

from sncsocket import SncSocket

class SncSocketClient(SncSocket):
    ''' socket client implementation '''

    def connect(self, host, port):
        ''' connects the socket to given host, port '''
        try: 
            self.s.connect((host, port))
        except:
            raise Exception('Failed connecting socket')

    def send(self, data):
        ''' sends data to connected server '''
        try:
            self.s.send(data)
        except:
            raise Exception('Failed sending data')
