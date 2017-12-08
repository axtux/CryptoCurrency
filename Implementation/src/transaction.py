import json


class Transaction(object):
    def __init__(self, sender, amount, receiver):
        self.sender = sender
        self.amount = amount
        self.receiver = receiver

    def toJson(self):
        return json.dumps({
                "sender":self.sender,
                "amount":self.amount,
                "receiver":self.receiver,
            })

    @staticmethod
    def fromJson(data):
        print(data)
        data= json.loads(data)
        return Transaction(**data)