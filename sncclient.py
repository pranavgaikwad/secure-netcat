# Author : Pranav Gaikwad

import sys
import select

from sncsocket import SncSocket

class SncSocketClient(SncSocket):
    ''' socket client implementation '''

    def _start(self):
        ''' main loop with select() '''
        std_input = sys.stdin
        # readable file descriptors
        readable_fds = [self.s, sys.stdin]
        # writeable file descriptors
        writeable_fds = []
        # buffer for data to be sent
        buffer_data = []
        # main loop
        while readable_fds:
            try:
                ready_for_read, ready_for_write, exceptions = select.select(readable_fds, writeable_fds, readable_fds)
                # ready for read 
                for descriptor in ready_for_read:
                    if descriptor is std_input:
                        read_data = std_input.readline()
                        if read_data:
                            buffer_data.append(read_data)
                            # make connection writeable
                            self._add_descriptor_to(writeable_fds, self.s)
                            # done with stdin for now
                            self._remove_descriptor_from(readable_fds, descriptor)

                    elif descriptor is self.s:
                        recvd_data = self.s.recv(SncSocket.MAX_BUFFER_SIZE)
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

                # ready for writing 
                for descriptor in ready_for_write:
                    if descriptor is self.s:
                        data_to_send = ''
                        for data in buffer_data:
                            data_to_send += data
                        if data_to_send:
                            descriptor.send(data_to_send)
                        self._add_descriptor_to(readable_fds, std_input)
                        self._add_descriptor_to(readable_fds, descriptor)
                        self._remove_descriptor_from(writeable_fds, descriptor)
                        buffer_data = []
                
                # exceptional descriptors
                for descriptor in exceptions:
                    self._remove_descriptor_from(readable_fds, descriptor)
                    self._remove_descriptor_from(writeable_fds, descriptor)
                    descriptor.close()
                    sys.exit(1)

            except (EOFError, KeyboardInterrupt):
                self._close()
                break

    def start(self, host, port):
        ''' starts the client '''
        try:
            self.s.connect((host, port))
            self._start()
        except Exception as e:
            raise Exception('Failed starting client : %s' % str(e))
