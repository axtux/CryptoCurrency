from utils import generateDSAKey, intToBytes, encrypt_AES, iv, decrypt_AES
from Crypto import Random
from hashlib import sha256
import math
import random

class Address(object):
    """The private and public key for the Wallet
    The public key is also the adresse to make transaction with the Wallet"""

    def __init__(self, AES_Key, addr=None):
        super(Address, self).__init__()
        print ("                     Good Morning !")
        print ("                  This is your AES Key")
        print ("It's REALLY important so, remenber it and NEVER forgive")
        print ("          "+AES_Key)

        if addr == None:
            self.iv = iv()
            self.privateKey = generateDSAKey()
            self.privateKey.x = encrypt_AES(bytes.fromhex(AES_Key), intToBytes(self.privateKey.x), self.iv)
            self.publicKey = self.privateKey.publickey()
            self.address = self.hash()
        else:
            self.address = addr
            #Check private and public key in BDD
            #Private key is still encrypt in the BDD with AES

    def signature(self, m):
        k = random.randint(2, self.publicKey.q - 1)
        return self.privateKey.sign()

    def hash(self):
        """Create a hash with the Public Key to make an adress
        The update function from hashlib add a string ton a list
        The hexdigest function from hashlib hash all the data send with update and return it in hexadecimal"""
        h = sha256()
        h.update(str(self.publicKey.y).encode('utf-8'))
        h.update(str(self.publicKey.g).encode('utf-8'))
        h.update(str(self.publicKey.p).encode('utf-8'))
        h.update(str(self.publicKey.q).encode('utf-8'))
        return h.hexdigest()
