'''
Author   : Pranav Gaikwad
Unity Id : 200203543
'''

import sys
import json
from base64 import b64encode, b64decode

from Crypto.Cipher import AES
from Crypto.Protocol import KDF
from Crypto.Random import get_random_bytes

class IntegrityError(Exception):
    pass

class InvalidMessageError(Exception):
    pass

class AesHelper:
    ''' encryption / decryption helper '''

    # program does not allow keys less than 16 characters long
    LENGTH_IDEAL_KEY = 16

    # these keys are expected in a typical encrypted msg
    MSG_KEYS = [ 'n', 'c', 't', 's' ]

    @staticmethod
    def encrypt(plaintext, key):
        ''' encrypts data using AES in GCM mode '''
        ''' and returns msg with tag, nonce, ciphertext & salt in it '''
        # generate a random salt or pepper or whatever
        salt = get_random_bytes(AesHelper.LENGTH_IDEAL_KEY)
        # derive key 
        key = AesHelper._derive_key(key, salt)
        # encrypt
        cipher = AES.new(key, AES.MODE_GCM)
        ciphertext, tag = cipher.encrypt_and_digest(plaintext)
        values = [ b64encode(value).decode('utf-8') for value in cipher.nonce, ciphertext, tag, salt ]
        
        return json.dumps(dict(zip(AesHelper.MSG_KEYS, values)))

    @staticmethod
    def decrypt_and_verify(ciphertext, key):
        ''' decrypts data encoded using AES '''
        try:
            b64 = json.loads(ciphertext)
            msg = { key: b64decode(b64[key]) for key in AesHelper.MSG_KEYS }
        except Exception as e:
            raise InvalidMessageError('Invalid message : %s\n'%str(e))

        key = AesHelper._derive_key(key, msg[AesHelper.MSG_KEYS[3]])
        
        cipher = AES.new(key, AES.MODE_GCM, nonce=msg[AesHelper.MSG_KEYS[0]])
        
        try: 
            plaintext = cipher.decrypt_and_verify(msg[AesHelper.MSG_KEYS[1]], msg[AesHelper.MSG_KEYS[2]])
        except Exception as e:
            raise IntegrityError('Integrity of message is compromised : %s'%str(e))

        return plaintext

    @staticmethod
    def _derive_key(password, salt):
        ''' derives PBKDF2 key from given key & password '''
        return KDF.PBKDF2(password, salt, dkLen=32)
