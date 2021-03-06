import sqlite3
from lib.address import Address


DB_PATH = 'databases/wallet.db'

def createDB():
    """Create all using data bases
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


def loadAddressList(user_ID):
    """Load a list with all address from the user
    """
    addrList = []
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""SELECT addr FROM addrList WHERE user_ID=? ORDER BY num""", (user_ID,))
    for addr in cursor.fetchall():
        addrList.append(Address.fromJson(addr[0]))
    conn.close()
    return addrList

def add_address(user_ID, newAddr, num):
    """Add the new actual address on the DB
       The last address on the list is the actual address
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""INSERT INTO addrList(user_ID, addr, num) VALUES(?,?,?)""", (user_ID, newAddr.toJson(), num))
    conn.commit()
    conn.close()

def userExist(user_ID, hashPassword):
    """Check in the DB if the user exist AND have enter the good password
       Return True if id and hashPassword of the user are correct
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""SELECT ID FROM users WHERE (ID=? AND hashPass=?)""", (user_ID, hashPassword))
    client = cursor.fetchone()
    conn.close()
    return not client is None

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
