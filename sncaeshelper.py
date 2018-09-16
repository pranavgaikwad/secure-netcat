# Author : Pranav Gaikwad
import sys
import json

from Crypto.Cipher import AES
from Crypto.Protocol import KDF
from base64 import b64encode, b64decode

class IntegrityError(Exception):
    pass

class InvalidMessageError(Exception):
    pass

class AesHelper:
    ''' encryption / decryption helper '''

    # these keys are expected in a typical encrypted msg
    MSG_KEYS = [ 'n', 'c', 't' ]

    @staticmethod
    def encrypt(plaintext, key):
        ''' encrypts data using AES in GCM mode '''
        ''' and returns msg with tag, nonce, & ciphertext in it '''
        cipher = AES.new(key, AES.MODE_GCM)
        ciphertext, tag = cipher.encrypt_and_digest(plaintext)
        values = [ b64encode(value).decode('utf-8') for value in cipher.nonce, ciphertext, tag ]
        return json.dumps(dict(zip(AesHelper.MSG_KEYS, values)))

    @staticmethod
    def decrypt_and_verify(ciphertext, key):
        ''' decrypts data encoded using AES '''
        try:
            b64 = json.loads(ciphertext)
            msg = { key: b64decode(b64[key]) for key in AesHelper.MSG_KEYS }
        except Exception as e:
            raise InvalidMessageError('Invalid message : %s\n'%str(e))

        cipher = AES.new(key, AES.MODE_GCM, nonce=msg[AesHelper.MSG_KEYS[0]])
        
        try: 
            plaintext = cipher.decrypt_and_verify(msg[AesHelper.MSG_KEYS[1]], msg[AesHelper.MSG_KEYS[2]])
        except Exception as e:
            raise IntegrityError('Integrity of message is compromised %s'%str(e))

        return plaintext

    @staticmethod
    def derive_key(password, salt):
        ''' derives PBKDF2 key from given key & password '''
        return KDF.PBKDF2(password, salt, dkLen=32)

# tests. 
# ignore this code. 
if __name__ == '__main__':

    key = 'RANDOMKEYSRANDOM'

    msg = AesHelper.encrypt('this is secret message', key)

    print msg

    print AesHelper.decrypt_and_verify(msg, key)