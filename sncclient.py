# Author : Pranav Gaikwad

import sys
import select

from sncsocket import SncSocket
from aeshelper import AesHelper, IntegrityError, InvalidMessageError

class SncSocketClient(SncSocket):
    ''' socket client implementation '''

    def _start(self, encryption_key):
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
                            for recvd_data_chunk in self._split_json_string(recvd_data):
                                decrypted_data = AesHelper.decrypt_and_verify(recvd_data_chunk, encryption_key)
                                self._print(decrypted_data)
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
                        # data_to_send = ''
                        for data in buffer_data:
                            encrypted_data = AesHelper.encrypt(data, encryption_key)
                            descriptor.send(encrypted_data)
                            # data_to_send += data
                        # if data_to_send:
                            # descriptor.send(data_to_send)
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
                sys.exit(0)

            except (IntegrityError, InvalidMessageError):
                self._close()
                self._eprint('Message integrity compromised')
                sys.exit(1)
    
    def start(self, host, port, encryption_key):
        ''' starts the client '''
        try:
            self.s.connect((host, port))
            self._start(encryption_key)
        except Exception as e:
            raise Exception('Failed starting client : %s' % str(e))
