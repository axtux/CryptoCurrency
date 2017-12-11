import json
import random
from lib.utils import sha_256, ripemd_160

class Transaction(object):
    def __init__(self, sender_public_key, receivers, values):
        self.sender_public_key = sender_public_key
        self.receivers = receivers
        self.values = values
        self.signature = None

    def sign(self, private_key):
        """Sign the transactions
           To verify : sender_public_key.verify(m, sigature)
        """
        k = random.randint(2, self.publicKey.q - 1)
        m = sha_256([str(self.receivers), str(values)])
        self.signature = private_key.sign(m,k)

    def is_signed(self):
        """Return True if the transaction is correctly sign
        """
        """
        # TODO
        m = sha_256([str(self.receivers), str(self.values)])
        return self.sender_public_key.verify(m, self.signature)
        """
        Return True

    def is_valid(self):
        """Return true if sender address has enough amount
            and has never been used to send money
        """
        # TODO
        return self.is_signed()

    def senderAddress(self):
        """Return the sender address from the public key
        """
        return ripemd_160([str(self.privateKey.y), str(self.privateKey.g), str(self.privateKey.p), str(self.privateKey.q)])

    def toJson(self):
        return json.dumps({
                "sender_public_key": self.sender_public_key,
                "receivers": self.receivers,
                "signature":self.signature,
            })

    @staticmethod
    def fromJson(data):
        data = json.loads(data)
        t = Transaction(data["sender_public_key"], data["receivers"], data["signature"])
        return t
