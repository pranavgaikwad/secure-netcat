'''
Author   : Pranav Gaikwad
Unity Id : 200203543
'''

import sys
import select

from sncsocket import SncSocket, SncSendError, SncReceiveError

class SncSocketServer(SncSocket):
    """ socket server implementation """

    MAX_CLIENTS = 5

    def _start(self, encryption_key):
        """ main server loop with select() call """
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
                ready_for_read, ready_for_write, exceptions = select.select(
                    readable_fds, writeable_fds, readable_fds)
                # file descriptors ready for reading
                for descriptor in ready_for_read:
                    # first time when server starts,
                    # a connection is accepted from client
                    if descriptor is self.s:
                        connection, client_addr = descriptor.accept()
                        connection.setblocking(0)
                        SncSocket._eprint('Received connection from [%s:%s]'%
                                          (str(client_addr[0]), str(client_addr[1])))
                        # add new connection to readable descriptors' list
                        SncSocket._add_descriptor_to(readable_fds, connection)
                        # make std_in readable
                        SncSocket._add_descriptor_to(readable_fds, std_input)
                        # make connection writeable
                        SncSocket._add_descriptor_to(writeable_fds, connection)
                        # remove the server from readable since we already have the connection
                        SncSocket._remove_descriptor_from(readable_fds, descriptor)
                    elif descriptor is std_input:
                        read_data = std_input.readline()
                        if read_data:
                            buffer_data.append(read_data)
                            # connection is ready to send new data
                            SncSocket._add_descriptor_to(writeable_fds, connection)
                            # once data is read, we want std_input removed from readable state
                            SncSocket._remove_descriptor_from(readable_fds, descriptor)
                    else:
                        valid = self._recv(descriptor, encryption_key)
                        if valid:
                            # make connection writeable
                            SncSocket._add_descriptor_to(writeable_fds, descriptor)
                            # make std_input readable
                            SncSocket._add_descriptor_to(readable_fds, std_input)
                        else:
                            SncSocket._remove_descriptor_from(readable_fds, std_input)
                            SncSocket._remove_descriptor_from(readable_fds, descriptor)
                            SncSocket._remove_descriptor_from(writeable_fds, descriptor)
                for descriptor in ready_for_write:
                    for data in buffer_data:
                        self._send(descriptor, data, encryption_key)
                    SncSocket._add_descriptor_to(readable_fds, std_input)
                    SncSocket._add_descriptor_to(readable_fds, descriptor)
                    SncSocket._remove_descriptor_from(writeable_fds, descriptor)
                    buffer_data = []
                for descriptor in exceptions:
                    SncSocket._remove_descriptor_from(readable_fds, descriptor)
                    SncSocket._remove_descriptor_from(writeable_fds, descriptor)
                    descriptor.close()
                    sys.exit(1)
            except (EOFError, KeyboardInterrupt, SncSendError, SncReceiveError):
                self._close()
                sys.exit(0)

    def start(self, port, encryption_key):
        """
        connects the socket to given host, port
        starts accepting connections and begins main loop
        """
        try:
            # non blocking mode
            self.s.setblocking(0)
            # bind to localhost
            self.s.bind(('', port))
            # start listening
            self.s.listen(SncSocketServer.MAX_CLIENTS)
            # main loop
            self._start(encryption_key)
        except Exception as error:
            self._close()
            raise Exception('Failed starting server : %s\n'%str(error))
