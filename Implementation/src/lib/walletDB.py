import sqlite3
import lib.address
from copy import deepcopy


DB_PATH = 'databases/client.db'

def createDB():
    """Create all using data base
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS addrList (
    	user_ID	TEXT NOT NULL,
    	addr	TEXT NOT NULL,
    	num	INTEGER NOT NULL
    );""")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
    	ID	TEXT PRIMARY KEY NOT NULL UNIQUE,
    	hashPass	TEXT NOT NULL
    );""")
    conn.commit()
    conn.close()


def loadAddressList(user_ID, password):
    """Load a list with all address from the user
    """
    addrList = []
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""SELECT addr FROM addrList WHERE user_ID=? ORDER BY num""", (user_ID,))
    for addr in cursor.fetchall():
        addrList.append(fromJson(addr[0]).decryptPrivateKey(password))
    conn.close()
    return addrList

def add_address(user_ID, newAddr, num, password):
    """Add the new actual address on the DB
       The last address on the list is the actual address
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    tmp = deepcopy(newAddr)
    tmp.encryptPrivateKey(password)
    cursor.execute("""INSERT INTO addrList(user_ID, addr, num) VALUES(?,?,?)""", (user_ID, tmp.toJson(), num))
    conn.commit()
    conn.close()

def userExist(user_ID, hashPassword):
    """Check in the DB if the user exist AND have enter the good password
       Return the actualAddress of the user if id and hashPassword are correct
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""SELECT ID FROM users WHERE (ID=? AND hashPass=?)""", (user_ID, hashPassword))
    client = cursor.fetchone()
    conn.close()
    return client != None

def newUser(user_ID, hashPassword):
    """Create a new user in the DB
       The new id cannot be already used in the DB
       return True when the new user was create, False if the user id was already used
    """
    ret = True
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("""INSERT INTO users(ID, hashPass) VALUES(?, ?)""", (user_ID, hashPassword))
        conn.commit()
    except sqlite3.IntegrityError:
        ret = False
    finally:
        conn.close()
        return ret
