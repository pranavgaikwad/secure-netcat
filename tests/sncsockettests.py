import sys
import unittest

sys.path.append('../')
import sncsocket

class SnsSocketTests(unittest.TestCase):
    ''' test cases for SnsSocket class '''
    def setUp(self):
        self.socket = sncsocket.SncSocket()

    def testSplitJsonString(self):
        json_string = '''{"nonce": "ChmaWd0ohfejPgNn6gIlsA==", "ciphertext": "8A==", "tag": "gWJAAYi2n7TJP4Jh4olTfA=="}{"nonce": "eE9XSYMrcm8W04+z5fYWsw==", "ciphertext": "NeozHJus0YcM5l2Ewnzv6SoPK+6DhyRo2AzRG0r4Yg==", "tag": "DC0AmcObWnDkRwkg2BxrvA=="}'''
        expected = [
            '{"nonce": "ChmaWd0ohfejPgNn6gIlsA==", "ciphertext": "8A==", "tag": "gWJAAYi2n7TJP4Jh4olTfA=="}', 
            '{"nonce": "eE9XSYMrcm8W04+z5fYWsw==", "ciphertext": "NeozHJus0YcM5l2Ewnzv6SoPK+6DhyRo2AzRG0r4Yg==", "tag": "DC0AmcObWnDkRwkg2BxrvA=="}'
        ]
        assert expected == self.socket._split_json_string(json_string)

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


if __name__ == '__main__':
    unittest.main()