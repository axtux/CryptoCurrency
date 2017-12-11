import random
import sqlite3

# local imports
from blockchain import Blockchain
from utils import sha_256
from address import Address

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
        self.user_ID = user_ID
        self.blockChain = Blockchain
        self.updateBlockchain()
        self.addrList = []
        self.loadAddressList()
        self.last = len(self.addrList)-1    #index of the actual address
        if self.addrList == []:    #New Wallet : Create the first Address
            self.addr = Address(AES_Key=AES_Key)
            self.addrList.append(self.addr.address)
            self.defineActualAddress(self.addr)
        else:
            self.addr = Address(addr=self.addrList[self.last])
        self.count = self.checkCount()

    def updateBlockchain(self):
        """Update the Blockchain
           Ask to the relay node the next block from the actual version of the blockchain
           Stop when the Blockchain is valid (next block is None)
        """
        lastBlock = self.blockChain.get_last_block()
        #newBlock = TODO ask to the relay node the nex block
        while newBlock != None:
            self.blockChain.add_block(newBlock)
            #newBlock = TODO ask to the relay node the nex block

    def checkCount(self):
        """Check, with the actual address, the Wallet value in the BlockChain
        """
        count = 0
        block = self.blockChain.get_next_block(self.blockChain.FIRST_HASH)
        while block != None:
            for trans in block.transactions:
                for dest,val in trans.receiver,trans.values:
                    if dest == self.addr.address:
                        count += val
            block = self.blockChain.get_next_block(block.get_hash())
        return count

    def createTransaction(self, moneyList, destList, AES_Key):
        """Create a new transaction and send it to the RelayNode
           moneyList[i] is the value send to the address destList[i]
           The last transaction is the rest of the wallet send to the new user address
        """
        # TODO
        newAddr = Address(AES_Key=AES_Key)
        if len(moneyList) == len(destList) and sum(moneyList) <= self.count:
            moneyList.append(self.count - sum(moneyList))
            destList.append(newAddr.address)
            transac = transaction(self.addr, moneyList, toList, newAddr)
            #network.postTransaction(transac)
            self.defineActualAddress(newAddr)

    def loadAddressList(self):
        """Load a list with all address from the user
        """
        conn = sqlite3.connect('../databases/client.db')
        cursor = conn.cursor()
        cursor.execute("""SELECT addr FROM addrList WHERE user_ID=? ORDER BY num""", (self.user_ID,))
        for addr in cursor.fetchall():
            self.addrList.append(addr[0])
        conn.close()

    def defineActualAddress(self, newAddr):
        """Define the newAddr as the actual address of the user
           Change it in the DB
        """
        conn = sqlite3.connect('../databases/client.db')
        cursor = conn.cursor()
        cursor.execute("""UPDATE users SET actualAddress=? WHERE ID=?""", (newAddr.address, self.user_ID))
        cursor.execute("""INSERT INTO addrList(user_ID, addr, num) VALUES(?,?,?)""", (self.user_ID, newAddr.address, len(self.addrList)))
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

    w = Wallet("prout", AES_Key=sha_256(password)[:32])
    print(w.addrList)
