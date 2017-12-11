import json


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
        self.signature = private_key.sign(str(sum(self.values)),k)

    def is_signed(self):
        """Return True if the transaction is correctly sign
        """
        return self.sender_public_key.verify(str(sum(self.values)), self.signature)

    def is_valid(self):
        """Return true if sender address has enough amount
            and has never been used to send money
        """
        # TODO
        return self.is_signed()

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
