import hashlib
import json

from transaction import Transaction

class Block:
    DIFFICULTY = 5
    MAX_TRANSACTIONS = 50

    def __init__(self, previous_hash, miner_address, transactions=[]):
        self.previous_hash = previous_hash
        self.miner_address = miner_address
        self.set_transactions(transactions)

    def set_transactions(transaction):
        # TODO: add transactions and update trasanctions_hash
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

    def __eq__(self,otherBloc):
        return self.__str__() == otherBloc.__str__()

    def setMinerAdress(self,adress):
        self.minerAdress=adress

    def hash(self, proof):
        # TODO: hash previous_hash, miner_address, transactions_hash and proof
        self.pow = proof
        h = hashlib.sha256()
        h.update(str(self) + str(proof))
        return h.digest()

    def is_valid():
        #TODO: check that hash correspond to DIFFICULTY
        pass

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
