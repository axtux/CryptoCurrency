import hashlib

class Block:
    def __init__(self, prevHash):
        self.transactions = []
        self.previousHash = prevHash
        self.pow = 0
        self.difficulty = 0
        self.size = 10  # Can be changed later

    def addTransaction(transaction):
        if(len(self.transactions) < self.size):
            self.transactions.append(transaction)
        else:
            raise BlocFull('The block is full')

    def __str__(self):
        tmp = ""
        tmp = tmp + str(self.previousHash)
        for t in self.transactions:
            tmp = tmp + str(i)
        return tmp

    def hash(self, proof):
        self.pow = proof
        h = hashlib.sha256()
        h.update(str(self) + str(proof))
        return h.digest()
