import sys
import json
import unittest

sys.path.append('../')
import sncsocket

class SnsSocketTests(unittest.TestCase):
    ''' test cases for SnsSocket class '''
    def setUp(self):
        self.socket = sncsocket.SncSocket()

    def testSplitJsonString(self):
        expected = [
            '{"s": "L0NnY1dh42lT2TVWZA2lQg==", "c": "JQ==", "t": "/1N5yuIKdF1LpAyAcS37rQ==", "n": "tVpnXLwmTPSrK1Vb1a5RJg=="}'
        ]
        json_string = open('testmessages', 'r').read()
        assert expected == self.socket._split_json(json_string)

        
    def testAddDescriptorTo(self):
        descriptors = []

        self.socket._add_descriptor_to(descriptors, self.socket.s)
        assert descriptors == [self.socket.s]

        self.socket._add_descriptor_to(descriptors, None)
        assert descriptors == [self.socket.s]

    def testRemoveDescriptorsFrom(self):
        descriptors = [self.socket.s]
        self.socket._remove_descriptor_from(descriptors, self.socket.s)
        assert descriptors == []

        descriptors = [self.socket.s]
        self.socket._remove_descriptor_from(descriptors, None)
        assert descriptors == [self.socket.s]

    def testReadLargeLines(self):
        read_data = sys.stdin.readline()

        assert read_data


if __name__ == '__main__':
    unittest.main()