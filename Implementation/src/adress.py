from utils import generateDSAKey, intToBytes, encrypt_AES, iv
from Crypto import Random
from hashlib import sha256
import math
import random

class adress(object):
    """The private and public key for the Wallet
    The public key is also the adresse to make transaction with the Wallet"""

    def __init__(self, AES_key):
        super(adress, self).__init__()
        self.iv = iv()
        self.privateKey = generateDSAKey()
        print("value of x :")
        print(self.privateKey.x)
        print("----")
        self.privateKey.x = encrypt_AES(bytes.fromhex(AES_key), intToBytes(self.privateKey.x), self.iv)
        self.publicKey = self.privateKey.publickey()
        self.adress = self.hash()
        print("value of x (encrypt) :")
        print(self.privateKey.x)
        print("----")

    def signature(self, m):
        k = random.randint(2, self.publicKey.q - 1)
        return self.privateKey.sign()

    def hash(self):
        h = sha256()
        h.update(str(self.publicKey.y).encode('utf-8'))
        h.update(str(self.publicKey.g).encode('utf-8'))
        h.update(str(self.publicKey.p).encode('utf-8'))
        h.update(str(self.publicKey.q).encode('utf-8'))
        return h.hexdigest()
