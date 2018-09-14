import sys
import unittest

sys.path.append('../')
import aeshelper

AesHelper = aeshelper.AesHelper

class AesHelperTests(unittest.TestCase):
    ''' Test cases for AES helper class '''
    def setUp(self):
        ''' sets up '''
        self.msg1 = 'this is a secret message'
        self.msg2 = 'this is another secret message'
        self.key = 'NOTSORANDOMKEY00'
        self.fakeKey = '000FAKEKEYISFAKE'

    def testEncrypt(self):
        encrypted_msg1 = AesHelper.encrypt(self.msg1, self.key)
        encrypted_msg2 = AesHelper.encrypt(self.msg2, self.key)

        assert encrypted_msg2 != encrypted_msg1
        assert encrypted_msg1 != self.msg1
        assert encrypted_msg2 != self.msg2

    def testDecrypt(self):
        encrypted_msg1 = AesHelper.encrypt(self.msg1, self.key)
        decrypted_msg1 = AesHelper.decrypt_and_verify(encrypted_msg1, self.key)
        assert decrypted_msg1 == self.msg1

        encrypted_msg2 = AesHelper.encrypt(self.msg2, self.key)
        decrypted_msg2 = AesHelper.decrypt_and_verify(encrypted_msg2, self.key)
        assert decrypted_msg2 == self.msg2

        encrypted_msg1 = AesHelper.encrypt(self.msg1, self.key)
        try:
            decrypted_msg1 = AesHelper.decrypt_and_verify(encrypted_msg1, self.fakeKey)
        except Exception as e:
            assert type(e) == aeshelper.IntegrityError

if __name__ == '__main__':
    unittest.main()