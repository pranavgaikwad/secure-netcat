# Author : Pranav Gaikwad

import re
import sys
import socket
from struct import pack, unpack

from aeshelper import AesHelper

class SncSocket:
    ''' generic class to handle common functions '''
    MAX_BUFFER_SIZE = 4096
    
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def _close(self):
        ''' closes server socket '''
        try:
            # self.s.shutdown()
            self.s.close()
        except:
            raise Exception('Failed closing socket')

    def _remove_descriptor_from(self, remove_from, descriptor):
        ''' removes given descriptor from given list of descriptors '''
        if descriptor in remove_from: 
            remove_from.remove(descriptor)

    def _add_descriptor_to(self, add_to, descriptor):
        ''' adds given descriptor in given list of descriptors '''
        if (descriptor not in add_to) and (descriptor is not None): 
            add_to.append(descriptor)

    def _print(self, msg):
        ''' prints to stdout '''
        sys.stdout.write('%s'%msg)

    def _eprint(self, msg):
        ''' prints to stderr '''
        sys.stderr.write('%s\n'%msg)

    def _split_json_string(self, msg):
        ''' splits a string containing multiple json '''
        ''' objects into list of json objects '''
        msg = msg.rstrip('\n')
        pattern = re.compile(r"}{")
        msg = pattern.sub("}\n{", msg)
        return msg.split('\n')

    def _split_json(self, msg):
        ''' splits json according to string sequence '''
        return re.findall(r'{"c": "[A-Za-z0-9/=\+]*", "t": "[A-Za-z0-9/=\+]*", "n": "[A-Za-z0-9/=\+]*"}', msg)

    def _send(self, descriptor, data, encryption_key):
        ''' sends message, handles encryption before sending '''
        encrypted_data = AesHelper.encrypt(data, encryption_key)
        encrypted_data = pack('>I', len(encrypted_data)) + encrypted_data
        descriptor.send(encrypted_data)

    def _recv(self, descriptor, encryption_key):
        ''' receives message, handles decryption after receiving '''
        # first 4 bytes are the length of the message sent by server
        recv_msg = descriptor.recv(4)
        # shows that no data / Ctrl+C was received
        if not recv_msg:
            return False 
        
        msg_length = unpack('>I', recv_msg)[0]

        # use buffer to receive all data no matter what size 
        recv_buffer = ''
        while len(recv_buffer) < msg_length:
            recvd_data = descriptor.recv(msg_length - len(recv_buffer))
            if recvd_data:
                recv_buffer += recvd_data
        
        for recvd_data_chunk in self._split_json(recv_buffer):
            decrypted_data = AesHelper.decrypt_and_verify(recvd_data_chunk, encryption_key)
            self._print(decrypted_data)
        
        return True   