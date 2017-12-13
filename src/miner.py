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
        self.block= Block(self.blockchain.get_last_hash(), self.address)
        self.block.set_transactions(self.get_transactions())
        self.index = 0

    def get_transactions(self):
        """Allow to choose wich transactions will be placed in the block
        For now, it just take them in the chronological order"""
        ts = self.relay.get_transactions()
        if ts is None:
            return []
        # filter invalid transactions
        ts = list(filter(lambda t: t.is_valid(self.blockchain), ts))
        # transactions can be valid alone and invalid together
        # (e.g. 2 transactions with same sender)
        if not self.block.valid_transactions(self.blockchain):
            self.block.set_transactions([])
        # TODO: sort as you want (fee ?)
        return ts

    def run(self,strategy):
        """Strategy is the function called to find the next PoW"""
        print('Mining for address '+str(self.address)+' ', end='')
        self.create_block()
        while(1):
            if self.flag == 0: # check relay for new block
                self.flag = Miner.FLAG
                if self.updater.update():
                    print('Downloaded new block')
                    print('Mining for address '+str(self.address)+' ', end='')
                    self.create_block()
                print('.', end='', flush=True) # show state to the user
            self.flag = self.flag - 1
            self.block.set_proof(strategy(self.index))
            self.index = self.index + 1
            if(self.block.good_difficulty()):
                print('\nMined block '+self.block.get_hash())
                self.relay.submit_block(self.block)
                self.flag = 0 #Need to take new transactions

def randompow(previousPow=0):
    return random.randint(0,2**256)

if __name__ == '__main__':
    argc = len(sys.argv)
    if not argc == 2:
        exit('usage: python3 '+sys.argv[0]+' YOUR_ADDRESS' )

    b = Blockchain('miner')
    miner = Miner(b, sys.argv[1])
    miner.run(randompow)
