import itertools  # List permutation methods
import utils
import block
import wallet  # Crypto methods
import Network.Miner
import random
import blockChain
class Miner:

     FLAG=10 #number of iteration of mining before check if the block has been found

    def __init__(self, blockchain, address, relay):
        self.blockChain = blockChain
        self.adress = address
        self.relay = relay
        self.flag=0

    def create_block(self):
        self.block= Block(self.blockChain.get_last_block().hash(),self.adress,self.get_ordered_transactions())


    def get_ordered_transactions(self):
        """Allow to choose wich transactions will be placed in the block
        For now, it just take them in the chronological order"""
        return self.relay.get_transactions()

    def run(self,strategy):
        """Strategy is the function called to find the next PoW"""
        self.create_block()
        while(1):
            if(self.flag == 0): #Check if a new block has been found
                self.flag = FLAG
                new_blockchain = self.relay.getBlockchain()
                if not (new_blockchain.get_last_block().hash()==self.blockChain.get_last_block().hash()): # New block has been found
                    self.blockchain = self.relay.getBlockchain()
                    self.create_block()
            else:
                self.flag = self.flag - 1
                self.mine(strategy)
                if(self.block.is_valid()):
                    self.relay.submit_block(self.block)
                    self.flag = 0 #Need to take new transactions




    def mine(self,strategy):
        digest = self.block.hash(strategy(self.bloc.pow))

    def increasepow(self,previousPow=0):
        return previousPow+1

    def decreasepow(self, previousPow=2**256):
        return previousPow-1

    def randompow(self,previousPow=0):
        return random.randint(0,2**256)
