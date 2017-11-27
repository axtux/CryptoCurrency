class bloc:
    def __init__(self):
        self.transactions=[]
        self.previousHash=0
        self.pow=0
        self.difficulty=0
        self.size=10 #On peut changer plus tard

    def addTransaction(transaction):
        if(len(self.transactions)<self.size):
            self.transactions.append(transaction)
        else:
            raise BlocFull('The bloc is full')
