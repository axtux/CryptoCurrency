import random
import sqlite3

# local imports
from lib.blockchain import Blockchain
from lib.utils import sha_256
from lib.address import Address

class Wallet(object):
    """Wallet is the principal user
    Wallet have money and can create some Transaction to send money to an another Wallet
    """

    def __init__(self, user_ID, AES_Key=None, addr=None):
        """Create a new wallet

        AES_key : The AES key of the user using to encrypt / decrypt his private key
        addr    : The current adress of the user
        """
        self.user_ID = user_ID
        self.bloackChain = self.askCopyChain()
        if addr == None:    #New Wallet : Create the first Address
            self.addr = Address(AES_Key=AES_Key)
            self.defineActualAddress(self.addr)
        else:
            self.addr = Address(addr=addr)
        self.count = self.checkCount()

    def askCopyChain(self):
        """Ask to the RelayNode a valid copy of the blockchain
        """
        # TODO
        return Blockchain()

    def checkCount(self):
        """Check, with the actual address, the Wallet value in the BlockChain
        """
        # TODO Ask to the relay node a copy of the BlockChain
        return 0

    def createTransaction(self, moneyList, destList, AES_Key):
        """Create a new transaction and send it to the RelayNode
           moneyList[i] is the value send to the address destList[i]
           The last transaction is the rest of the wallet send to the new user address
        """
        newAddr = Address(AES_Key=AES_Key)
        if len(moneyList) == len(destList) and sum(moneyList) <= self.count:
            moneyList.append(self.count - sum(moneyList))
            destList.append(newAddr.address)
            transac = transaction(self.addr, moneyList, toList, newAddr)
            #network.postTransaction(transac)
            self.defineActualAddress(newAddr)

    def signature(self, m):
        """return the Public Key object and the result of the signature
        To verify : publicKey.verify(m, signature)
        (see Crypto.PublicKey.DSA lib)
        """
        return self.actualKey.publicKey, self.actualKey.signature(m)

    def defineActualAddress(self, newAddr):
        """Define the newAddr as the actual address of the user
           Change it in the DB
        """
        conn = sqlite3.connect('client.db')
        cursor = conn.cursor()
        cursor.execute("""UPDATE users SET actualAddress=? WHERE ID=?""", (newAddr.address, self.user_ID))
        conn.commit()
        conn.close()
        self.addr = newAddr

if __name__ == '__main__':
    """
    w = Wallet()
    k = w.actualKey
    print(hex(k.publicKey.y))
    print(hex(k.publicKey.g))
    print(hex(k.publicKey.p))
    print(hex(k.publicKey.q))
    print(k.privateKey.x)
    print(utils.bytesToInt(utils.decrypt_AES(bytes.fromhex("5369787465656e2062797465206b6579"), k.privateKey.x, k.iv)))
    print("-----")
    print(k.address)
    """
    password = "veryGoodPassword"
    print(sha_256(password)[:32])

    w = Wallet(AES_Key=sha_256(password)[:32])
    print(w.addr)
    newAddr = Address()
    w.defineActualAddress(newAddr)
    print(w.addr)
