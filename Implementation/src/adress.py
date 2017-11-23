from Crypto.Util import number
import math

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
        self.publicKey = 1
        self.privateKey = 1
