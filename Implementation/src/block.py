import hashlib
import json

from transaction import Transaction

class Block:
    def __init__(self, previousHash,transactions=[],pow=0,difficulty=0,size=10):
        self.transactions = transactions
        self.previousHash = previousHash
        self.pow = pow    #proofOfWork
        self.difficulty = difficulty
        self.size = size  # Can be changed later

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

    def toJson(self):
        return json.dumps({
                "transactions": [v.toJson() for v in self.transactions] ,
                "previousHash":self.previousHash,
                "pow":self.pow,
                "difficulty":self.difficulty,
                "size":self.size,
            })

    @staticmethod
    def fromJson(data):
        data= json.loads(data)
        transactions= [Transaction.fromJson(v) for v in data.pop("transactions")]
        return Block(transactions=transactions, **data)