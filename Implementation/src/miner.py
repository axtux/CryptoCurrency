import itertools  # List permutation methods
import utils
import bloc
import wallet  # Crypto methods
import Network.Miner
import random
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

    def __init__(self, blockchain, address, relay):
        self._transactions = []
        self._mining = 0
        self.wallet = wallet()
        self.bloc = Miner.getWork()

    def run(self,strategy):
        testBloc= Miner.getWork()
        if (self.bloc.__eq__(testBloc)): #Test if the bloc has not been found by other miner
            hash=self.mine(strategy)
            if(self.isBlocValid()):
                #submitBloc
        else:
            self.bloc=test.bloc



     def mine(self,strategy):
        digest = self.bloc.hash(strategy(self.bloc.pow))
        return digest

    def isBlocValid(self):
        check = True
        digest = self.bloc.hash(self.bloc.pow)
        for (i in range(0, self.bloc.difficulty)):
            if not digest[i] == "0" :
                check = False
        return check

    def submitTransactions():
        """Gives transactions in order that gives good value to a relay node
        """
        pass

    def increasepow(self,previousPow):
        return previousPow+1

    def decreasepow(self, previousPow):
        return previousPow-1

    def randompow(self,previousPow):
        return random.randint(0,2**256)
