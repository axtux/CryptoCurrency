import sqlite3

# local imports
from lib.blockchain import Blockchain
from lib.utils import sha_256
from lib.address import Address
from lib.updater import Updater
from lib.walletDB import loadAddressList, add_address
from lib.http_client import RelayClient
from lib.transaction import Transaction

class Wallet(object):
    """Wallet is the principal user
    Wallet have money and can create some Transaction to send money to an another Wallet
    """

    def __init__(self, user_ID, password):
        """Create a new wallet

        user_ID  : The ID of the user to select it's own address on the DB
        password : The password is used to generate a AES_Key to ecrypt / decrypt the private key on DB
                   Here, we used it to load all the address or write the new address
        """
        #self.blockChain = Blockchain()
        #self.relay = RelayClient()
        #self.updater = Updater(self.blockChain, self.relay)
        #self.updater.update()
        self.user_ID = user_ID
        self.addrList = loadAddressList(self.user_ID)   # list of address
        self.last = len(self.addrList)-1    #index of the actual address
        if self.addrList == []:    #New Wallet : Create the first Address
            self.addr = Address()
            self.addr.encryptPrivateKey(password)
            add_address(self.user_ID, self.addr, 0)
            self.addrList.append(self.addr)
        else:
            self.addr = self.addrList[len(self.addrList)-1]
        #self.count = self.blockChain.get_amount_of_address(self.addr)
        self.count = 80

    def checkUpdate(self):
        """Update the amount and the blockChain
        """
        self.updater.update()
        self.count = self.blockChain.get_amount_of_address(self.addr)

    def createTransaction(self, password, destList):
        """Create a new transaction and send it to the RelayNode
           destList is a list of tuples
           Each tuples is like : (str_address, value)
           The last transaction is the rest of the wallet send to the new user address
        """
        # TODO
        #self.checkUpdate()
        newAddr = Address()
        newAddr.encryptPrivateKey(password)
        total = sum([ i[1] for i in destList ])
        if total <= self.count:
            destList.append( (str(newAddr), (self.count - total)) )
            transac = Transaction(self.addr.public(), destList)
            self.addr.decryptPrivateKey(password)
            transac.sign(self.addr)
            self.addr.encryptPrivateKey(password)
            #self.relay.submit_transaction(transac)
            self.addrList.append(newAddr)
            self.addr = newAddr
            add_address(self.user_ID, self.addr, len(self.addrList)-1)
            return transac
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
