from Crypto.Util import number
from Crypto.PublicKey import DSA
import random


def generatePrime(n):
     """Generate a N-bit Prime Number"""
     return number.getPrime(n)
