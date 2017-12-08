import itertools  # List permutation methods
import utils
import bloc
import wallet  # Crypto methods

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

    def __init__(self):
        self._transactions = []
        self._mining = 0
        self.wallet = wallet()
        self.bloc = bloc()

    def act(self):
        #TODO check if new transaction with relay node
        mine()
        if(isBlocValid()):
            #TODO send bloc to relay node
            pass

     def mine(self):
        digest = self.bloc.hash(self.bloc.pow + 1)
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