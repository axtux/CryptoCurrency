from utils import sha_256
from address import Address
from wallet import Wallet
import sqlite3

class Connection(object):
    """Wallet connection
    The user uses it to connect him to his wallet
    """

    def __init__(self):
        pass

    def allowConnection(self, id, password, newWallet=False):
        """Create or connecte to a wallet

        id          : The identification of the user
        password    : The password of the user
        newWallet   : True to create a new wallet with these information
                      False to connecte to user to his Wallet
        """
        if newWallet:
            if self.newUser(id, sha_256(password)[:8] + sha_256(password)[24:]):
                return Wallet(AES_Key=sha_256(password)[8:24])
        else:
            addr = self.userExist(id, sha_256(password)[:8] + sha_256(password)[24:])
            if addr:
                return Wallet(addr=addr)
        return None

    def userExist(self, id, hashPassword):
        """Check in the DB if the user exist AND have enter the good password
           Return the actualAddress of the user if id and hashPassword are correct
        """
        conn = sqlite3.connect('client.db')
        cursor = conn.cursor()
        cursor.execute("""SELECT actualAddress FROM users WHERE (ID=? AND hashPass=?)""", (id, hashPassword))
        client = cursor.fetchone()
        conn.close()
        if client != None:
             return client[0]
        return False

    def newUser(self, id, hashPassword):
        """Create a new user in the DB
           The new id cannot be already used in the DB
           return True when the new user was create, False if the user id was already used
        """
        ret = True
        conn = sqlite3.connect('client.db')
        cursor = conn.cursor()
        try:
            cursor.execute("""INSERT INTO users(ID, hashPass) VALUES(?, ?)""", (id, hashPassword))
            cursor.execute("""SELECT * FROM users""")
            conn.commit()
        except sqlite3.IntegrityError:
            ret = False
        finally:
            conn.close()
            return ret

    def addrList(self, id):
        """Return a list of Address object with all address of the user in the DB
        """
        return []



if __name__ == '__main__':
    password = "veryGoodPassword"
    print(sha_256(password).encode('utf-8'))
    print(len(sha_256(password)))
    print(sha_256(password)[:8] + sha_256(password)[24:])
