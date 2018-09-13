# Author : Pranav Gaikwad

import sys
import select
import traceback

from sncsocket import SncSocket

class SncSocketServer(SncSocket):
    ''' socket server implementation '''

    MAX_CLIENTS = 5

    def _start(self):
        ''' main server loop with select() call '''
        std_input = sys.stdin
        # readable file descriptors
        readable_fds = [self.s, std_input]
        # writeable file descriptors
        writeable_fds = []
        # buffer to store messages
        buffer_data = []
        # assuming that only one client will be connected at a time
        connection = None
        # start the loop
        while readable_fds:
            try:
                ready_for_read, ready_for_write, exceptions = select.select(readable_fds, writeable_fds, readable_fds)
                
                # file descriptors ready for reading
                for descriptor in ready_for_read:
                    # first time when server starts,
                    # a connection is accepted from client
                    if descriptor is self.s:
                        connection, client_addr = descriptor.accept()
                        connection.setblocking(0)
                        self._eprint('Received connection from [%s:%s]\n'%(str(client_addr[0]),str(client_addr[1])))
                        # add new connection to readable descriptors' list
                        self._add_descriptor_to(readable_fds, connection)
                        # make std_in readable
                        self._add_descriptor_to(readable_fds, std_input)
                        # make connection writeable
                        self._add_descriptor_to(writeable_fds, connection)
                        # remove the server from readable since we already have the connection
                        self._remove_descriptor_from(readable_fds, descriptor)

                    elif descriptor is std_input:
                        read_data = std_input.readline()
                        if read_data:
                            buffer_data.append(read_data)
                            # connection is ready to send new data
                            self._add_descriptor_to(writeable_fds, connection)
                            # once data is read, we want std_input removed from readable state
                            self._remove_descriptor_from(readable_fds, descriptor)

                    else:
                        recvd_data = descriptor.recv(SncSocket.MAX_BUFFER_SIZE)
                        if recvd_data:
                            self._print(recvd_data)
                            # make connection writeable
                            self._add_descriptor_to(writeable_fds, descriptor)
                            # make std_input readable
                            self._add_descriptor_to(readable_fds, std_input)
                        else:
                            self._remove_descriptor_from(readable_fds, std_input)
                            self._remove_descriptor_from(readable_fds, descriptor)
                            self._remove_descriptor_from(writeable_fds, descriptor)

                for descriptor in ready_for_write:
                    data_to_send = ''
                    for data in buffer_data:
                        data_to_send += data
                    if data_to_send:
                        descriptor.send(data_to_send)
                    self._add_descriptor_to(readable_fds, std_input)
                    self._add_descriptor_to(readable_fds, descriptor)
                    self._remove_descriptor_from(writeable_fds, descriptor)
                    buffer_data = []

                for descriptor in exceptions:
                    self._remove_descriptor_from(readable_fds, descriptor)
                    self._remove_descriptor_from(writeable_fds, descriptor)
                    descriptor.close()
                    sys.exit(1)
            
            except (EOFError, KeyboardInterrupt):
                self._close()
                sys.exit(0)

    def start(self, port):
        ''' connects the socket to given host, port '''
        ''' starts accepting connections and begins main loop '''
        try:
            # non blocking mode
            self.s.setblocking(0)
            # bind to localhost
            self.s.bind(('', port))
            # start listening
            self.s.listen(SncSocketServer.MAX_CLIENTS)
            # main loop
            self._start()
        except Exception as e:
            raise Exception('Failed starting server : %s' % str(traceback.format_exc()))
