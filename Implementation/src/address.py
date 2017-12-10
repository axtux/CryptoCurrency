import math
import random
from hashlib import sha256
from Crypto import Random
from utils import generateDSAKey, buildDSAKey, intToBytes, encrypt_AES, iv, decrypt_AES, sha_256
import sqlite3

class Address(object):
    """The private and public key for the Wallet
    The public key is also the adresse to make transaction with the Wallet
    """

    def __init__(self, AES_Key=None, addr=None):
        if addr == None:    #Generate  a new address
            self.iv = iv()
            self.privateKey = generateDSAKey()
            self.privateKey.x = encrypt_AES(AES_Key, intToBytes(self.privateKey.x), self.iv)
            self.publicKey = self.privateKey.publickey()
            self.address = self.hash() # TODO Not good
            self.recordAddress()
        else:   #Load an existing address
            self.address = addr
            key, key_pr = self.loadKey()
            self.privateKey = buildDSAKey(key, key_pr)
            self.publicKey = self.privateKey.publickey()


    def signature(self, m):
        k = random.randint(2, self.publicKey.q - 1)
        return self.privateKey.sign()

    def loadKey(self):
        """Load the public / private key from the DB
           The private key is still encrypt with AES in the DB
        """
        conn = sqlite3.connect('client.db')
        cursor = conn.cursor()
        cursor.execute("""SELECT pkey_y, pkey_g, pkey_p, pkey_q, prkey_x FROM addresses WHERE address=?""", (self.address,))
        keys = cursor.fetchone()
        key = (int(keys[0]),int(keys[1]),int(keys[2]),int(keys[3]))
        conn.close()
        return key, keys[4]

    def recordAddress(self):
        """Write the actual key and address on the DB
           Change the previous "actual address" to an "old address"
        """
        conn = sqlite3.connect('client.db')
        cursor = conn.cursor()
        cursor.execute("""INSERT INTO addresses(address,pkey_y,pkey_g,pkey_p,pkey_q,prkey_x) VALUES(?,?,?,?,?,?)""",\
                        (self.address, str(self.privateKey.y), str(self.privateKey.g), str(self.privateKey.p), str(self.privateKey.q), self.privateKey.x))
        conn.commit()
        conn.close()

    def hash(self):
        """Create a hash with the Public Key to make an adress
        The update function from hashlib add a string ton a list
        The hexdigest function from hashlib hash all the data send with update and return it in hexadecimal
        """
        h = sha256()
        h.update(str(self.publicKey.y).encode('utf-8'))
        h.update(str(self.publicKey.g).encode('utf-8'))
        h.update(str(self.publicKey.p).encode('utf-8'))
        h.update(str(self.publicKey.q).encode('utf-8'))
        return h.hexdigest()


if __name__ == '__main__':
    password = "veryGoodPassword"
    key = sha_256(password)[:32].encode('utf-8')
    mess = "bonjour"
    #iv = iv()

    a = Address(AES_Key=key)
    addr = a.address
    print(a.privateKey.y)
    print(a.privateKey.g)
    print(a.privateKey.p)
    print(a.privateKey.q)
    print(a.privateKey.x)
    b = Address(addr=addr)
    print("------")
    print(a.privateKey.y == b.privateKey.y)
    print(a.privateKey.g == b.privateKey.g)
    print(a.privateKey.p == b.privateKey.p)
    print(a.privateKey.q == b.privateKey.q)
    print(a.privateKey.x == b.privateKey.x)

"""
    c = encrypt_AES(key,mess,iv)
    e = decrypt_AES(key,c,iv)
    print(e.decode('utf-8'))
"""
