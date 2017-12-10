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

    def set_transactions(transactions):
        # TODO: add transactions and update trasanctions_hash
        self.transactions=[]
        for i in transactions:
            if len(self.transactions) < MAX_TRANSACTIONS:
                self.transactions.append(i)
            else:
                break
        h= hashlib.sha256()
        for i in self.transactions:
            h.update(i.toJson().encode('utf-8'))
        self.transactions_hash = h.digest()

    def setMinerAdress(self,adress):
        self.minerAdress=adress

    def hash(self, proof=self.pow):
        # TODO: hash previous_hash, miner_address, transactions_hash and proof
        self.pow = proof
        h = hashlib.sha256()
        h.update(self.previous_hash.encode('utf-8'))
        h.update(self.miner_address.encode('utf-8'))
        h.update(self.transactions_hash).encode('utf-8')
        h.update(str(proof).encode('utf-8'))
        return h.digest()

    def is_valid():
        test = self.hash(self.pow)
        check=True
        for i in range(0,DIFFICULTY):
            if (not (test[i]=="0")):
                check = False
        return check



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
