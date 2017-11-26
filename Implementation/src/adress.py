import utils
import math
import random

class adress(object):
    """The private and public key for the Wallet
    The public key is also the adresse to make transaction with the Wallet"""
    def __init__(self):
        super(adress, self).__init__()
        self.publicKey = 1
        self.privateKey = 1 #must be encrypt with AES
        self.generate()

    def generate(self):
        """Generate a private and public key"""
        self.privateKey = utils.generateDSAKey()    # Encrypt with AES
        self.publicKey = self.privateKey.publickey()

    def signature(self, m):
        k = random.randint(2, self.publicKey.q - 1)
        return self.privateKey.sign()
