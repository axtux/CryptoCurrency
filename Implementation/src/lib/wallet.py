import random
import sqlite3

# local imports
from lib.blockchain import Blockchain
from lib.utils import sha_256
from lib.address import Address
from lib.updater import Updater
from lib.walletDB import loadAddressList
from lib.http_client import RelayClient

class Wallet(object):
    """Wallet is the principal user
    Wallet have money and can create some Transaction to send money to an another Wallet
    """

    def __init__(self, user_ID, password):
        """Create a new wallet

        user_ID  : The ID of the user to select it's own address on the DB
        password : The password is used to generate a AES_Key and ecrypt / decrypt the private key on DB
                   Here, we used it to load all the address or write the new address
        """
        self.blockChain = Blockchain()
        self.relay = RelayClient()
        self.updater = Updater(self.blockChain, self.relay)
        self.updater.update()
        self.user_ID = user_ID
        self.addrList = loadAddressList(self.user_ID, password)   # list of address
        self.last = len(self.addrList)-1    #index of the actual address
        if self.addrList == []:    #New Wallet : Create the first Address
            self.addr = Address()
            add_address(self.user_ID, self.addr, 0, password)
            self.addrList.append(self.addr)
        else:
            self.addr = self.addrList[len(self.addrList)-1]
        self.count = self.blockChain.get_amount_of_address(self.addr)

    def checkUpdate(self):
        """Update the amount and the blockChain
        """
        # TODO peut-être la mettre dans Updater
        self.updater.update()
        self.count = self.blockChain.get_amount_of_address(self.addr)

    def createTransaction(self, password, destList):
        """Create a new transaction and send it to the RelayNode
           moneyList[i] is the value send to the address destList[i]
           The last transaction is the rest of the wallet send to the new user address
        """
        # TODO
        self.checkUpdate()
        hashPass = sha_256(password)
        newAddr = Address()
        if len(moneyList) == len(destList) and sum(moneyList) <= self.count:
            destList.append( str(newAddr), (self.count - sum(moneyList)) )
            transac = transaction(self.addr.public(), destList)
            transac.sign(self.addr)
            self.relay.submit_transaction(transac)
            self.addrList.append(newAddr)
            self.addr = newAddr
            add_address(self.user_ID, self.addr, len(self.addrList)-1, password)
            return True
        else:
            return False

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

    w = Wallet("prout", AES_Key=sha_256(password)[:32])
    print(w.addrList)
