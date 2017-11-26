from Crypto.Util import number
from Crypto.PublicKey import DSA
import random


def generatePrime(n):
     """Generate a N-bit Prime Number"""
     return number.getPrime(n)

def generateDSAKey():
    """Generate a DSA Key"""
    return DSA.generate(3072)      #3072 is recomend by the NIST 800-57



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
