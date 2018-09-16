'''
Author   : Pranav Gaikwad
Unity Id : 200203543
'''

import re
import sys
import socket
from struct import pack, unpack

from sncaeshelper import AesHelper, IntegrityError, InvalidMessageError

class SncSendError(Exception):
    """ socket send operation failed """
    pass

class SncReceiveError(Exception):
    """ socket recv operation failed """
    pass

class SncSocket(object):
    """ generic class to handle common functions """
    MAX_BUFFER_SIZE = 2048

    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def _close(self):
        """ closes server socket """
        try:
            # self.s.shutdown()
            self.s.close()
        except:
            raise Exception('Failed closing socket')

    @staticmethod
    def _remove_descriptor_from(remove_from, descriptor):
        """ removes given descriptor from given list of descriptors """
        if descriptor in remove_from:
            remove_from.remove(descriptor)

    @staticmethod
    def _add_descriptor_to(add_to, descriptor):
        """ adds given descriptor in given list of descriptors """
        if (descriptor not in add_to) and (descriptor is not None):
            add_to.append(descriptor)

    @staticmethod
    def _print(msg):
        """ prints to stdout """
        sys.stdout.write('%s'%msg)

    @staticmethod
    def _eprint(msg):
        """ prints to stderr """
        sys.stderr.write('%s\n'%msg)

    @staticmethod
    def _get_recv_size(msg_length, buffer_length):
        """
        returns ideal message size to receive
        based on msg_length, buffer_len & max_buffer_size
        """
        remaining_msg_size = msg_length - buffer_length
        if remaining_msg_size > SncSocket.MAX_BUFFER_SIZE:
            return SncSocket.MAX_BUFFER_SIZE
        return remaining_msg_size

    def _send(self, descriptor, data, encryption_key):
        """ sends message, handles encryption before sending """
        encrypted_data = AesHelper.encrypt(data, encryption_key)
        encrypted_data = pack('>I', len(encrypted_data)) + encrypted_data
        try:
            descriptor.send(encrypted_data)
        except Exception as error:
            raise SncSendError('Error sending data : %s'%str(error))

    def _recv(self, descriptor, encryption_key):
        """ receives message, handles decryption after receiving """
        # first 4 bytes are the length of the message sent by server
        recv_msg = descriptor.recv(4)
        # shows that no data / Ctrl+C was received
        if not recv_msg:
            return False

        msg_length = unpack('>I', recv_msg)[0]

        try:
            # use buffer to receive all data no matter what size
            recv_buffer = ''
            while len(recv_buffer) < msg_length:
                recvd_data = descriptor.recv(self._get_recv_size(msg_length, len(recv_buffer)))
                if recvd_data:
                    recv_buffer += recvd_data
        except Exception as error:
            raise SncReceiveError('Error receiving data : %s'%str(error))

        try:
            for recvd_data_chunk in AesHelper.split_msgs(recv_buffer):
                if recvd_data_chunk:
                    decrypted_data = AesHelper.decrypt_and_verify(recvd_data_chunk, encryption_key)
                    self._print(decrypted_data)
        except (IntegrityError, InvalidMessageError) as error:
            self._close()
            self._eprint('Message integrity compromised : %s'%str(error))
            sys.exit(1)
        return True
