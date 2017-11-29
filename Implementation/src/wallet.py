from adress import adress
import random
import utils

class wallet(object):
    """Wallet is the principal user
    Wallet have money and can create some Transaction to send money to an another Wallet"""

    def __init__(self):
        super(wallet, self).__init__()
        self.actualKey = adress("5369787465656e2062797465206b6579")
        self.oldKey = []
        self.count = 0

    def createTransaction(self, money, to):
        """Create a new transaction to send it to the RelayNode"""
        transac = transaction(self.adress, money, to) #Class a créer
        return None

    def signature(self, m):
        """return the Public Key object and the result of the signature
            To verify : publicKey.verify(m, signature)
            (see Crypto.PublicKey.DSA lib)"""
        return self.actualKey.publicKey, self.actualKey.signature(m)



w = wallet()
k = w.actualKey
print(hex(k.publicKey.y))
print(hex(k.publicKey.g))
print(hex(k.publicKey.p))
print(hex(k.publicKey.q))
print(k.privateKey.x)
print(utils.bytesToInt(utils.decrypt_AES(bytes.fromhex("5369787465656e2062797465206b6579"), k.privateKey.x, k.iv)))
print("-----")
print(k.adress)
