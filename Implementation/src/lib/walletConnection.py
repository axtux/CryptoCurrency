import sqlite3

# local imports
from lib.utils import sha_256
from lib.wallet import Wallet
from lib.walletDB import createDB, userExist, newUser

class Connection(object):
    """Wallet connection
       The user uses it to connect him to his wallet
    """

    def __init__(self):
        createDB()
        pass

    def allowConnection(self, user_ID, password, newWallet=False):
        """Create or connecte to a wallet

        user_ID     : The identification of the user
        password    : The password of the user
        newWallet   : True to create a new wallet with these information
                      False to connecte to user to his Wallet
        """
        hashPass = sha_256(password)
        if newWallet:
            if newUser(user_ID, hashPass[:16] + hashPass[48:]):
                return Wallet(user_ID, password)
        else:
            if userExist(user_ID, hashPass[:16] + hashPass[48:]):
                return Wallet(user_ID, password)
        return None





if __name__ == '__main__':
    password = "veryGoodPassword"
    conn = Connection()
    w = conn.allowConnection("prout",password)
    a = Address(addr="12")
    w.defineActualAddress(a)
