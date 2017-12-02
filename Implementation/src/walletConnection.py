from utils import sha_256
from address import Address
from wallet import Wallet

class Connection(object):
    """Wallet connection
       The user uses it to connect him to his wallet"""

    def __init__(self):
        super(Connection, self).__init__()

    def allowConnection(self, id, password, newWallet=False):
        """Create or connecte to a wallet

        id          : The identification of the user
        password    : The password of the user
        newWallet   : True to create a new wallet with these information
                      False to connecte to user to his Wallet"""


        if newWallet:
            self.createUser(id, sha_256(password)[:16]+sha_256(password[:48]))
            return Wallet(AES_Key=sha_256(password)[16:48])
        elif self.userExist(id, sha_256(password)[:16]+sha_256(password[:48])):
            #check id and password (hash [:16]+[48:]) in the DB
            addr = []   #Add the principal address on the first position
            for ad in self.addrList(id): #All address in the DB
                addr.append(ad)
            return Wallet(addr=addr)
        else:
            return None

    def userExist(self, id, hashPassword):
        """Check in the DB if the user exist AND have enter the good password"""
        #Check
        return True

    def addrList(self, id):
        """Return a list of Address object with all address of the user in the DB"""
        return []

    def createUser(self, id, hashPassword):
        """Create a new Wallet on the DB"""
        #DB creation
        pass




conn = Connection()
w = conn.allowConnection("prout", "megaPassword")
print(w.count)
