import sqlite3

# local imports
from lib.utils import sha_256
from lib.address import Address
from lib.wallet import Wallet

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
        hashPass = sha_256(password)
        if newWallet:
            if self.newUser(id, hashPass[:16] + hashPass[48:]):
                return Wallet(id, AES_Key=hashPass[16:48])
        else:
            addr = self.userExist(id, hashPass[:16] + hashPass[48:])
            if addr:
                return Wallet(id, addr=addr)
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
        conn = sqlite3.connect('../databases/client.db')
        cursor = conn.cursor()
        try:
            cursor.execute("""INSERT INTO users(ID, hashPass, actualAddress) VALUES(?, ?, ?)""", (id, hashPassword, ""))
            conn.commit()
        except sqlite3.IntegrityError:
            ret = False
        finally:
            conn.close()
            return ret

    def createDB(self):
        """Create all using data base
        """
        conn = sqlite3.connect('../databases/client.db')
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS addrList (
        	user_ID	TEXT NOT NULL,
        	addr	TEXT NOT NULL,
        	num	INTEGER NOT NULL
        );""")

        cursor.execute("""
            CREATE TABLE addresses (
        	address	TEXT PRIMARY KEY NOT NULL,
        	pkey_y	TEXT NOT NULL,
        	pkey_g	TEXT NOT NULL,
        	pkey_p	TEXT NOT NULL,
        	pkey_q	TEXT NOT NULL,
        	prkey_x	BLOB NOT NULL
        );""")

        cursor.execute("""
            CREATE TABLE users (
        	ID	TEXT PRIMARY KEY NOT NULL UNIQUE,
        	hashPass	TEXT NOT NULL,
        	actualAddress	TEXT NOT NULL UNIQUE
        );""")
        conn.commit()
        conn.close()


if __name__ == '__main__':
    password = "veryGoodPassword"
    conn = Connection()
    w = conn.allowConnection("prout",password)
    a = Address(addr="12")
    w.defineActualAddress(a)
