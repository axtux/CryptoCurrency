import lib.utils
from lib.block import Block
import random
import sys
from lib.blockchain import Blockchain
import lib.updater
from lib.network import Network
from lib.http_client import RelayClient
from lib.updater import Updater

class Miner:
    FLAG=1e6 #number of iteration of mining before check if the block has been found

    def __init__(self, blockchain, address):
        self.blockchain = blockchain
        self.address = address
        self.relay = RelayClient()
        self.updater = Updater(self.blockchain, self.relay)
        self.flag=0
        self.index=0

    def create_block(self):
        self.block= Block(self.blockchain.get_last_hash(),self.address,self.get_ordered_transactions())
        # remove transactions if not valid
        if not self.block.valid_transactions(self.blockchain):
            self.block.set_transactions([])

    def get_ordered_transactions(self):
        """Allow to choose wich transactions will be placed in the block
        For now, it just take them in the chronological order"""
        ts = self.relay.get_transactions()
        if ts is None:
            return []
        return ts

    def run(self,strategy):
        """Strategy is the function called to find the next PoW"""
        self.create_block()
        while(1):
            if(self.flag == 0): #Check if a new block has been found
                self.flag = Miner.FLAG
                if self.updater.update(): # New block has been found
                    self.create_block()
            self.flag = self.flag - 1
            self.mine(strategy)
            if(self.block.good_difficulty()):
                self.relay.submit_block(self.block)
                self.flag = 0 #Need to take new transactions

    def mine(self,strategy):
        self.block.set_proof(strategy(self.index))
        self.index = self.index +1

def randompow(previousPow=0):
    return random.randint(0,2**256)

if __name__ == '__main__':
    argc = len(sys.argv)
    if not argc == 2:
        exit('usage: python3 '+sys.argv[0]+' YOUR_ADDRESS' )

    print('Starting miner with address '+str(sys.argv[1]))
    b = Blockchain('miner')
    miner = Miner(b, sys.argv[1])
    miner.run(randompow)
