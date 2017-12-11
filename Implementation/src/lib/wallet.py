import random
import sqlite3

# local imports
from lib.blockchain import Blockchain
from lib.utils import sha_256
from lib.address import Address
from lib.updater import Updater
from lib.walletDB import loadAddressList
from lib.http_client import RelayNode

class Wallet(object):
    """Wallet is the principal user
    Wallet have money and can create some Transaction to send money to an another Wallet
    """

    def __init__(self, user_ID, AES_Key=None, addr=None):
        """Create a new wallet

        user_ID : The ID of the user to select it's own address on the DB
        AES_key : The AES key of the user using to encrypt / decrypt his private key
        addr    : The current adress of the user
        """
        self.blockChain = Blockchain()
        self.relay = RelayNode()
        self.updater = Updater(self.blockChain, self.relay)
        self.updater.update()
        self.user_ID = user_ID
        self.addrList = loadAddressList(self.user_ID)
        self.last = len(self.addrList)-1    #index of the actual address
        if self.addrList == []:    #New Wallet : Create the first Address
            self.addr = Address(AES_Key=AES_Key)
            self.addrList.append(self.addr.address)
            self.defineActualAddress(self.addr)
        else:
            self.addr = Address(addr=self.addrList[self.last])
        self.count = self.blockChain.get_amount_of_address(self.addr)

    def checkUpdate(self):
        """Update the amount and the blockChain
        """
        # TODO peut-être la mettre dans Updater
        self.updater.update()
        self.count = self.blockChain.get_amount_of_address(self.addr)

    def checkCount(self):
        """Check, with the actual address, the Wallet value in the BlockChain
        """
        # TODO Methode non utile, à déplacé dans blockChain ou supprimé
        count = 0
        block = self.blockChain.get_next_block(self.blockChain.FIRST_HASH)
        while block != None:
            for trans in block.transactions:
                for dest,val in trans.receiver,trans.values:
                    if dest == self.addr.address:
                        count += val
            block = self.blockChain.get_next_block(block.get_hash())
        return count

    def createTransaction(self, password, moneyList, destList, AES_Key):
        """Create a new transaction and send it to the RelayNode
           moneyList[i] is the value send to the address destList[i]
           The last transaction is the rest of the wallet send to the new user address
        """
        # TODO
        self.checkUpdate()
        hashPass = sha_256(password)
        newAddr = Address(AES_Key=hashPass[16:48])
        if len(moneyList) == len(destList) and sum(moneyList) <= self.count:
            moneyList.append(self.count - sum(moneyList))
            destList.append(newAddr.address)
            transac = transaction(self.addr.publicKey, destList, moneyList)
            self.relay.submit_transaction(transac)
            self.addrList.append(newAddr.address)
            self.addr = newAddr
            add_address(self.user_ID, self.addr, len(self.addrList)-1)

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
