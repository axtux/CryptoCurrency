import math
import random
from hashlib import sha256
from Crypto import Random
import sqlite3

# local imports
from lib.utils import generateDSAKey, buildDSAKey, intToBytes, encrypt_AES, iv, decrypt_AES, ripemd_160
from lib.walletDB import loadKey, recordAddress

class Address(object):
    """The private and public key for the Wallet
    The public key is also the adresse to make transaction with the Wallet
    """

    def __init__(self, AES_Key=None, addr=None):
        if addr == None:    #Generate  a new address
            self.iv = iv()
            self.privateKey = generateDSAKey()
            self.privateKey.x = encrypt_AES(AES_Key, intToBytes(self.privateKey.x), self.iv)
            self.publicKey = self.privateKey.publickey()
            self.address = self.generateAddress()
            recordAddress(self.address, self.publicKey.y, self.publicKey.g, self.publicKey.p, self.publicKey.q, self.privateKey.x)
        else:   #Load an existing address
            self.address = addr
            self.privateKey, self.iv = loadKey(self.address)
            self.publicKey = self.privateKey.publickey()

    def generateAddress(self):
        """Create a hash with the Public Key to make an adress
        """
        return ripemd_160([str(self.privateKey.y), str(self.privateKey.g), str(self.privateKey.p), str(self.privateKey.q)])


if __name__ == '__main__':
    password = "veryGoodPassword"
    key = sha_256(password)[:32].encode('utf-8')
    mess = "bonjour"
    #iv = iv()

    a = Address(AES_Key=key)
    addr = a.address
    print(a.privateKey.y)
    print(a.privateKey.g)
    print(a.privateKey.p)
    print(a.privateKey.q)
    print(a.privateKey.x)
    b = Address(addr=addr)
    print("------")
    print(a.privateKey.y == b.privateKey.y)
    print(a.privateKey.g == b.privateKey.g)
    print(a.privateKey.p == b.privateKey.p)
    print(a.privateKey.q == b.privateKey.q)
    print(a.privateKey.x == b.privateKey.x)

"""
    c = encrypt_AES(key,mess,iv)
    e = decrypt_AES(key,c,iv)
    print(e.decode('utf-8'))
"""
