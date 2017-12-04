import math
import random
from hashlib import sha256
from Crypto import Random
from utils import generateDSAKey, intToBytes, encrypt_AES, iv, decrypt_AES


class Address(object):
    """The private and public key for the Wallet
    The public key is also the adresse to make transaction with the Wallet
    """

    def __init__(self, AES_Key=None, addr=None):
        if addr == None:    #Generate  a new address
            self.iv = iv()
            self.privateKey = generateDSAKey()
            self.privateKey.x = encrypt_AES(bytes.fromhex(AES_Key), intToBytes(self.privateKey.x), self.iv)
            self.publicKey = self.privateKey.publickey()
            self.address = self.hash()
        else:   #Load an existing address
            self.address = addr
            #Check private and public key in DB
            #Private key is still encrypt in the DB with AES

    def signature(self, m):
        k = random.randint(2, self.publicKey.q - 1)
        return self.privateKey.sign()

    def hash(self):
        """Create a hash with the Public Key to make an adress
        The update function from hashlib add a string ton a list
        The hexdigest function from hashlib hash all the data send with update and return it in hexadecimal
        """
        h = sha256()
        h.update(str(self.publicKey.y).encode('utf-8'))
        h.update(str(self.publicKey.g).encode('utf-8'))
        h.update(str(self.publicKey.p).encode('utf-8'))
        h.update(str(self.publicKey.q).encode('utf-8'))
        return h.hexdigest()
