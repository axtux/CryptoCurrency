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

def intToBytes(n):
    return n.to_bytes((n.bit_length()+7) // 8, 'big')

def bytesToInt(b):
    return int.from_bytes(b, 'big')

def encrypt_AES(key, m, iv):
    """Encrypt a byte string plainText with a key and a random iv
    """
    return bytesToInt(AES.new(key, AES.MODE_CFB, iv).encrypt(m))

def decrypt_AES(key, m, iv):
    """Decrypt a byte string cipherText with a key and a random iv
    """
    return AES.new(key, AES.MODE_CFB, iv).decrypt(intToBytes(m))

def generateAESKey():
    """Generate a random AES-128 key
        The "0x" at the begining of the hex number is remove for some function (bytes.fromhex)
    """
    return hex(random.getrandbits(128))[2:]

def iv():
    return Random.new().read(AES.block_size)

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
    #Some test
    key = DSA.generate(1024)
    m = b"Hello World !"
    sig = key.sign(m, 2)

    publicKey = key.publickey()
    if publicKey.verify(m,sig):
        print("Ok")
    else:
        print("Pas OK")
    """


    #AES-128 test
    mess = b'Hello World !'
    # key1 and key2 are the same keys
    key1 = b'Sixteen byte key'

    iv = Random.new().read(AES.block_size)
    ci = encrypt_AES(key1, mess, iv)
    pl = decrypt_AES(key1, ci, iv)
    print(ci)
    print(pl)
