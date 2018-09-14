# Author : Pranav Gaikwad

import re
import sys
import socket

class SncSocket:
    ''' generic class to handle common functions '''
    MAX_BUFFER_SIZE = 2048
    
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
        pattern = re.compile(r"}(.*){")
        msg = pattern.sub("}\n{", msg)
        return msg.split('\n')
