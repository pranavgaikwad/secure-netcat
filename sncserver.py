# Author : Pranav Gaikwad

from sncsocket import SncSocket

class SncSocketServer(SncSocket):
    ''' socket server implementation '''

    MAX_CLIENTS = 5
    MAX_BUFFER_SIZE = 1024

    def start(self, port):
        ''' connects the socket to given host, port '''
        ''' also accepts the connection & returns connection socket '''
        try: 
            self.s.bind(('', port))
            self.s.listen(SncSocketServer.MAX_CLIENTS)
            return self.s.accept()
        except:
            raise Exception('Failed starting server')


