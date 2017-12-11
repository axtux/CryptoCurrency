import json
import random
from lib.utils import sha_256_bytes, ripemd_160

class Transaction(object):
    def __init__(self, sender_public_key, receivers):
        """sender_public_key: Address object
        receivers: array of tuples (str_address, value)
        """
        # avoid transporting private key with transaction
        self.sender_public_key = sender_public_key.public()
        self.receivers = receivers
        self.signature = None
    
    def sign(self, private_key):
        """Sign the transactions
           private_key: Address object
        """
        if private_key.public() != self.sender_public_key:
            return False
        k = random.randint(2, private_key.dsa.q - 1)
        m = sha_256_bytes(self.toJson(False))
        self.signature = private_key.dsa.sign(m,k)

    def is_signed(self):
        """Return True if the transaction is correctly sign
        """
        if self.signature is None:
            return False
        m = sha_256_bytes(self.toJson(False))
        return self.sender_public_key.dsa.verify(m, self.signature)

    def get_total_amount(self):
        """Return total amount of money processed
        """
        total = 0
        for addr, amount in self.receivers:
            if amount < 1:
                return False
            total += amount
        return total

    def is_valid(self, blockchain):
        """Return true if sender address has enough amount
            and has never been used to send money
        """
        total = self.get_total_amount()
        if total == False or total < 1:
            return False
        available = blockchain.get_amount_of_address(self.sender_public_key)
        if available < 1:
            return False
        fee = available - total
        return self.is_signed() and fee >= 0

    def senderAddress(self):
        """Return the sender address from the public key
        """
        return ripemd_160([str(self.sender_public_key.y), str(self.sender_public_key.g), str(self.sender_public_key.p), str(self.sender_public_key.q)])

    def toJson(self, signature=True):
        return json.dumps({
                "sender_public_key": self.sender_public_key.toJson(),
                "receivers": self.receivers,
                "signature": self.signature if signature else None,
            })

    @staticmethod
    def fromJson(data):
        data = json.loads(data)
        sender_public_key = Address.fromJson(data["sender_public_key"])
        t = Transaction(sender_public_key, data["receivers"], data["signature"])
        return t
