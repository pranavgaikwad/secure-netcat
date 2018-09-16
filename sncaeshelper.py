'''
Author   : Pranav Gaikwad
Unity Id : 200203543
'''

from base64 import b64encode, b64decode

from Crypto.Cipher import AES
from Crypto.Protocol import KDF
from Crypto.Random import get_random_bytes


class IntegrityError(Exception):
    """ custom error when integrity of message could not be guaranteed """
    pass


class InvalidMessageError(Exception):
    """ message could not be parsed / incomplete message received """
    pass


class AesHelper(object):
    """ encryption / decryption helper """

    # program does not allow keys less than 16 characters long
    LENGTH_IDEAL_KEY = 16

    # two fields in a msg are separated using
    SEPARATOR_FIELDS = '__||'
    # two messages are separated using
    SEPARATOR_MSGS = '||__'

    @staticmethod
    def split_msgs(msgs):
        """ splits one single msg into different encrypted msgs using msg separator """
        return msgs.split(b64encode(AesHelper.SEPARATOR_MSGS).decode('utf-8'))

    @staticmethod
    def _split_msg(msg):
        """ splits a single message into different fields """
        return msg.split(b64encode(AesHelper.SEPARATOR_FIELDS).decode('utf-8'))

    @staticmethod
    def encrypt(plaintext, key):
        """
        encrypts data using AES in GCM mode
        and returns msg with tag, nonce, ciphertext & salt in it
        """
        # generate a random salt or pepper or whatever
        salt = get_random_bytes(AesHelper.LENGTH_IDEAL_KEY)
        # derive key
        key = AesHelper._derive_key(key, salt)
        # encrypt
        cipher = AES.new(key, AES.MODE_GCM)
        ciphertext, tag = cipher.encrypt_and_digest(plaintext)
        values = [
            b64encode(value).decode('utf-8')
            for value in cipher.nonce, ciphertext, tag, salt, AesHelper.SEPARATOR_MSGS
            ]

        return str(b64encode(AesHelper.SEPARATOR_FIELDS).decode('utf-8').join(values))

    @staticmethod
    def decrypt_and_verify(ciphertext, key):
        """ decrypts data encoded using AES """
        try:
            msg = AesHelper._split_msg(ciphertext)
        except Exception as error:
            raise InvalidMessageError('Invalid message : %s\n' % str(error))

        key = AesHelper._derive_key(key, b64decode(msg[3]))

        cipher = AES.new(key, AES.MODE_GCM, nonce=b64decode(msg[0]))

        try:
            plaintext = cipher.decrypt_and_verify(
                b64decode(msg[1]), b64decode(msg[2]))
        except Exception as error:
            raise IntegrityError(
                'Integrity of message is compromised : %s' % str(error))

        return plaintext

    @staticmethod
    def _derive_key(password, salt):
        """ derives PBKDF2 key from given key & password """
        return KDF.PBKDF2(password, salt, dkLen=32)
