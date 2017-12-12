import json
import random

# local imports
from lib.utils import sha_256_bytes
from lib.log import debug
from lib.address import Address

"""API

sign(Address)
is_signed()
get_total_amount(): get amount of sent money (can be < available if fee > 0)
is_valid(blockchain): signed and amount <= available amount on sender address
senderAddress(): string
toJson(): serialize
fromJson(): serialize
"""

class Transaction(object):
    def __init__(self, sender_public_key, receivers):
        """sender_public_key: Address object
        receivers: array of tuples (str_address, value)
        """
        # avoid transporting private key with transaction
        self.sender_public_key = sender_public_key.public()
        # JSON jump needed to have save representation and same signature
        self.receivers = json.loads(json.dumps(receivers))
        self.signature = None

    def sign(self, private_key):
        """Sign the transactions
           private_key: Address object
        """
        if private_key.public() != self.sender_public_key:
            return False
        # TODO use true random number :-/
        k = random.randint(2, private_key.dsa.q - 1)
        m = sha_256_bytes(str(self.sender_public_key)+str(self.receivers))
        self.signature = private_key.dsa.sign(m,k)

    def is_signed(self):
        """Return True if the transaction is correctly sign
        """
        if self.signature is None:
            debug('no signature')
            return False
        m = sha_256_bytes(str(self.sender_public_key)+str(self.receivers))
        signed = self.sender_public_key.dsa.verify(m, self.signature)
        if not signed:
            debug('bad signature')
        return signed

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
            debug('total amount of transaction < 1')
            return False
        available = blockchain.get_amount_of_address(self.sender_public_key)
        if available < 1:
            debug('amount available < 1')
            return False
        fee = available - total
        if fee < 0:
            debug('available('+str(available)+') < total('+str(total)+')')
            return False
        return self.is_signed()

    def senderAddress(self):
        """Return the sender address from the public key
        """
        return str(self.sender_public_key)

    def toJson(self):
        return json.dumps({
                "sender_public_key": self.sender_public_key.toJson(),
                "receivers": self.receivers,
                "signature": self.signature,
            })

    @staticmethod
    def fromJson(data):
        data = json.loads(data)
        sender_public_key = Address.fromJson(data["sender_public_key"])
        t = Transaction(sender_public_key, data["receivers"])
        t.signature = data["signature"]
        return t
