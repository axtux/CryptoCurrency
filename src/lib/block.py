import hashlib
import json

# local imports
from lib.transaction import Transaction
from lib.log import debug, warning

class Block:
    DIFFICULTY = 6
    MAX_TRANSACTIONS = 50

    def __init__(self, previous_hash, miner_address, transactions=[]):
        self.previous_hash = previous_hash
        self.miner_address = miner_address
        self.set_transactions(transactions)
        self.set_proof('')

    def set_transactions(self, transactions):
        # add a maximum of transactions
        self.transactions = transactions[:Block.MAX_TRANSACTIONS]
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

    def valid_transactions(self, blockchain):
        # only one transaction per sender
        senders = [t.senderAddress() for t in self.transactions]
        if len(senders) != len(set(senders)):
            warning('at least 2 transactions from sender '+sender)
            return False
        # check amount from senders
        for t in self.transactions:
            if not t.is_valid(blockchain):
                warning('at least one invalid transaction')
                return False
        return True

    def good_difficulty(self):
        return self.hash[:Block.DIFFICULTY] == '0'* Block.DIFFICULTY

    def is_valid(self, blockchain):
        return self.valid_transactions(blockchain) and self.good_difficulty()

    def toJson(self):
        return json.dumps({
                "previous_hash": self.previous_hash,
                "miner_address": self.miner_address,
                "proof": self.proof,
                "transactions": [t.toJson() for t in self.transactions],
            })

    @staticmethod
    def fromJson(json_data):
        try:
            data = json.loads(json_data)
            b = Block(data["previous_hash"], data["miner_address"])
            ts = []
            for t in data["transactions"]:
                ts.append(Transaction.fromJson(t))
            b.set_transactions(ts)
            b.set_proof(data["proof"])
            return b
        # JSON ValueError for decode
        # KeyError if no accessed key
        except (ValueError, KeyError, TypeError):
            return None
