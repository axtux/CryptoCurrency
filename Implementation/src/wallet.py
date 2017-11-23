import adress

class waller(object):
    """Wallet is the principal user
    Wallet have money and can create some Transaction to send money to an another Wallet"""

    def __init__(self):
        super(waller, self).__init__()
        self.actualKey = adress()
        self.oldKey = []

    def createTransaction(self, transacList):
        """Create a new transaction to send it to the RelayNode"""

        return None
