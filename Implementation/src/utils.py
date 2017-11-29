from Crypto.Util import number
from Crypto.PublicKey import DSA
from Crypto.Cipher import AES
from Crypto import Random
import random


def generatePrime(n):
     """Generate a N-bit Prime Number"""
     return number.getPrime(n)

def intToBytes(n):
    return n.to_bytes((n.bit_length()+7) // 8, 'big')

def bytesToInt(b):
    return int.from_bytes(b, 'big')

def generateDSAKey():
    """Generate a DSA Key"""
    return DSA.generate(1024)      #3072 is recomend by the NIST 800-57

def encrypt_AES(key, m, iv):
    """Encrypt a byte string plainText with a key and a random iv"""
    return AES.new(key, AES.MODE_CFB, iv).encrypt(m)

def decrypt_AES(key, m, iv):
    """Decrypt a byte string cipherText with a key and a random iv"""
    return AES.new(key, AES.MODE_CFB, iv).decrypt(m)

def generateAESKey():
    """Generate a random AES-128 key
        The "0x" at the begining of the hex number is remove for some function (bytes.fromhex)"""
    return hex(random.getrandbits(128))[2:]

def iv():
    return Random.new().read(AES.block_size)


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

"""
#AES-128 test
mess = b'Hello World !'
# key1 and key2 are the same keys
key1 = b'Sixteen byte key'
key2 = bytes.fromhex("5369787465656e2062797465206b6579")

iv = Random.new().read(AES.block_size)
iv2 = Random.new().read(AES.block_size)
ci = encrypt_AES(key2, mess, iv)
pl = decrypt_AES(key2, ci, iv)
print(key1)
print(key2)
print(ci)
print(pl)
"""
