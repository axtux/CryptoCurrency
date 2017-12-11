import hashlib
import json

# local imports
from lib.transaction import Transaction

class Block:
    DIFFICULTY = 5
    MAX_TRANSACTIONS = 50

    def __init__(self, previous_hash, miner_address, transactions=[]):
        self.previous_hash = previous_hash
        self.miner_address = miner_address
        self.set_transactions(transactions)

    def set_transactions(self, transactions):
        # add valid transactions
        self.transactions = []
        for t in transactions:
            if not t.is_valid():
                continue
            if len(self.transactions) >= self.MAX_TRANSACTIONS:
                break
            self.transactions.append(t)
        # update transactions hash
        h = hashlib.sha256()
        for i in self.transactions:
            h.update(i.toJson().encode('utf-8'))
        self.transactions_hash = h.hexdigest()

    def set_proof(self, proof):
        # hash previous_hash, miner_address, transactions_hash and proof
        self.proof = proof
        h = hashlib.sha256()
        h.update(self.previous_hash.encode('utf-8'))
        h.update(self.miner_address.encode('utf-8'))
        h.update(self.transactions_hash.encode('utf-8'))
        h.update(str(proof).encode('utf-8'))
        self.hash = h.hexdigest()
    
    def get_hash(self):
        return self.hash

    def is_valid(self):
        """Check that hash starts with some zeroes
        """
        return self.hash[:DIFFICULTY] == '0'*DIFFICULTY

    def toJson(self):
        return json.dumps({
                "previous_hash": self.previous_hash,
                "miner_address": self.miner_address,
                "proof": self.proof,
                "transactions": [t.toJson() for t in self.transactions],
            })

    @staticmethod
    def fromJson(data):
        try:
            data = json.loads(data)
        except TypeError:
            return None
        b = Block(data["previous_hash"], data["miner_address"])
        ts = []
        for t in data["transactions"]:
            ts.append(Transaction.fromJson(t))
        b.set_transactions(ts)
        return b
