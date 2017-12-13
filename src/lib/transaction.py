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
        self.receivers = receivers
        # sign only if private key included
        self.sign(sender_public_key)

    def data_to_sign(self):
        return sha_256_bytes(self.toJson(False))

    def sign(self, private_key):
        """Sign the transaction
           private_key: Address object
        """
        if private_key.public() != self.sender_public_key:
            return False
        self.signature = private_key.sign(self.data_to_sign())

    def is_signed(self):
        """Return True if the transaction is correctly signed
        """
        return self.sender_public_key.good_signature(self.data_to_sign(), self.signature)

    def get_total_amount(self):
        """Return total amount of money processed
        """
        total = 0
        for addr, amount in self.receivers:
            if amount < 1:
                debug('amount < 1')
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

    def toJson(self, includeSingature=True):
        data = {}
        data['sender_public_key'] = self.sender_public_key.toJson()
        data['receivers'] = self.receivers
        if includeSingature:
            data['signature'] = self.signature
        # sort keys for consistency
        return json.dumps(data, sort_keys=True)

    @staticmethod
    def fromJson(data):
        data = json.loads(data)
        sender_public_key = Address.fromJson(data["sender_public_key"])
        t = Transaction(sender_public_key, data["receivers"])
        t.signature = data["signature"]
        return t
