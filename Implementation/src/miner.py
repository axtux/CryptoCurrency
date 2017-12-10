import itertools  # List permutation methods
import utils
import block
import wallet  # Crypto methods
import Network.Miner
import random
import blockChain
class Miner:
    """A Miner gives the proof of work to give the first step of confirmation for a transaction
    Miners contain
     - the list of the transactions on which there working
     - flag to show that they are working
     - amount of money they own
    They can
     - request transactions
     - mine them
     - send packages of transactions to relmay nodes once they'r good enough
     """
     FLAG=10 #number of iteration of mining before check if the block has been found

    def __init__(self, blockchain, address, relay):
        self.blockChain = blockChain
        self.adress = address
        self.relay = relay
        self.flag=0

    def create_block(self):
        self.block= Block(self.blockChain.get_last_block().hash(),self.adress,self.get_ordered_transactions())

    def get_ordered_transactions(self):
        return self.relay.get_transactions()

    def run(self,strategy):
        self.create_block()
        while(1):
            if(self.flag == 0):
                self.flag = FLAG
                new_blockchain = self.relay.getBlockchain()
                if not (new_blockchain.get_last_block().hash()==self.blockChain.get_last_block().hash()): # New block has been found
                    self.blockchain = self.relay.getBlockchain()
                    self.create_block()
            else:
                self.flag = self.flag - 1
                self.mine(strategy)
                if(self.block.is_valid()):
                    self.relay.submitBlock(self.block)
                    self.flag = 0 #Need to take new transactions




     def mine(self,strategy):
        digest = self.block.hash(strategy(self.bloc.pow))



    def submitTransactions():
        """Gives transactions in order that gives good value to a relay node
        """
        pass

    def increasepow(self,previousPow=0):
        return previousPow+1

    def decreasepow(self, previousPow=2**256):
        return previousPow-1

    def randompow(self,previousPow=0):
        return random.randint(0,2**256)
