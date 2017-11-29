from adress import adress
import random
import utils

class wallet(object):
    """Wallet is the principal user
    Wallet have money and can create some Transaction to send money to an another Wallet"""

    def __init__(self, AES_Key=None, addr=None):
        """Create a new wallet

        AES_key : The AES from the user using to encrypt / decrypt his private key
                If the AES_Key was not correct, the private key will not be correct and not be able to sign a transaction
        addr    : The current adress from the user
                If the addr was not correct, the AES_Key will not be able to sign a transaction
                """

        super(wallet, self).__init__()
        if AES_Key == None:
            self.actualKey = adress(utils.generateAESKey(), addr)
        else:
            self.actualKey = adress(AES_Key, addr)
        self.oldKey = []
        self.count = 0

    def createTransaction(self, money, to):
        """Create a new transaction to send it to the RelayNode"""
        transac = transaction(self.adress, money, to)
        self.oldKey.append(self.adress)
        #New adrees
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
