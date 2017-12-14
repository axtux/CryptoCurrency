from Crypto.Util import number
from Crypto.Cipher import AES
from Crypto import Random
from hashlib import sha256
from hashlib import new as ripemd160
import random
import json


def generatePrime(n):
     """Generate a N-bit Prime Number
     """
     return number.getPrime(n)

def iv():
    return Random.new().read(AES.block_size).hex()

def intToBytes(n):
    return n.to_bytes((n.bit_length()+7) // 8, 'big')

def bytesToInt(b):
    return int.from_bytes(b, 'big')

def aes(pwd, iv):
    h = sha_256(pwd)
    return AES.new(h[16:48], AES.MODE_CFB, bytes.fromhex(iv))

def sha_256(text):
    """hash the content of text
       text : String or list of String
    """
    h = sha256()
    if type(text) == str:
        h.update(text.encode('utf-8'))
    else: #type(text) == list
        for i in text:
            h.update(i.encode('utf-8'))
    return h.hexdigest()

def sha_256_bytes(text):
    """hash the content of text
       text : String or list of String
    """
    h = sha256()
    if type(text) == str:
        h.update(text.encode('utf-8'))
    else: #type(text) == list
        for i in text:
            h.update(i.encode('utf-8'))
    return h.digest()

def ripemd_160(text):
    """hash the content of text
       text : String or list of String
    """
    h = ripemd160('ripemd160')
    if type(text) == str:
        h.update(text.encode('utf-8'))
    else: #type(text) == list
        for i in text:
            h.update(i.encode('utf-8'))
    return h.hexdigest()


if __name__ == '__main__':

    """
     the next lines are some tests of our functions
    """
    key = DSA.generate(1024)
    m = b"Hello World !"
    sig = key.sign(m, 2)

    publicKey = key.publickey()
    if publicKey.verify(m,sig):
        print("Ok")
    else:
        print("Pas OK")



    password = "veryGoodPassword"
    hashPass = sha_256(password)

    #AES-128 test
    mess = 55
    # key1 and key2 are the same keys
    key1 = 'Sixteen byte key'

    #iv = Random.new().read(AES.block_size)
    key = hashPass[16:48]
    iv = hashPass[:16]
    ci = encrypt_AES(key, mess, iv)
    pl = decrypt_AES(key, ci, iv)
    print(ci)
    print(pl)
