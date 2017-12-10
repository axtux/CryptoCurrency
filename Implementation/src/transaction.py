import json


class Transaction(object):
    def __init__(self, sender_public_key, receivers):
        self.sender = sender
        self.receivers = receivers

    def toJson(self):
        return json.dumps({
                "sender":self.sender,
                "amount":self.amount,
                "receiver":self.receiver,
            })

    def sign(self, private_key):
        pass

    def is_signed():
        pass

    @staticmethod
    def fromJson(data):
        data= json.loads(data)
        return Transaction(**data)
