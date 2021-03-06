import json
from Crypto.Random import random
from Crypto.PublicKey import DSA

# local imports
from lib.utils import ripemd_160, aes, iv

class Address(object):
    """manage DSA asymetric keys and adds some methods
    used as private and public key for the Wallet
    """
    def __init__(self, dsa=DSA.generate(1024), iv=iv()):
        self.dsa = dsa
        self.iv = iv

    def __str__(self):
        """Create hash from public key to make an address
        """
        k = self.dsa
        return ripemd_160([str(k.y), str(k.g), str(k.p), str(k.q)])

    def __eq__(self, other):
        return self.toJson() == other.toJson()

    def public(self):
        return Address(self.dsa.publickey())

    def sign(self, data):
        """expect data as bytes
        """
        if not self.dsa.has_private():
            return
        k = random.StrongRandom().randint(1,self.dsa.q-1)
        return self.dsa.sign(data, k)

    def good_signature(self, data, signature):
        """expect data as bytes and signature as tuple returned by sign()
        """
        if signature is None:
            return False
        return self.dsa.verify(data, signature)

    def encryptPrivateKey(self, password):
        """Encrypt the private key with AES
        """
        if not self.dsa.has_private():
            return False
        # encoding key as numeric string is fine
        self.enc = aes(password, self.iv).encrypt(str(self.dsa.x)).hex()
        # only public key
        self.dsa = self.dsa.publickey()
        return True

    def decryptPrivateKey(self, password):
        """DEcrypt the private key with AES
        """
        if self.dsa.has_private() or self.enc is None:
            return False
        # decode int from numeric string
        try:
            x = int(aes(password, self.iv).decrypt(bytes.fromhex(self.enc)))
        except ValueError:
            return False
        # build private key
        d = self.dsa
        self.dsa = DSA.construct((d.y, d.g, d.p, d.q, x))
        self.enc = None
        return True

    def toJson(self):
        data = {}
        # public key fields
        data['y'] = self.dsa.y
        data['g'] = self.dsa.g
        data['p'] = self.dsa.p
        data['q'] = self.dsa.q
        # private key (optionnal)
        try:
            data['x'] = self.dsa.x
        except AttributeError:
            pass
        try:
            data['enc'] = self.enc
            data['iv'] = self.iv
        except AttributeError:
            pass
        # sort keys for consistency
        return json.dumps(data, sort_keys=True)

    @staticmethod
    def fromJson(json_dsa):
        try:
            data = json.loads(json_dsa)
            if 'x' in data: # private key
                t = (data['y'], data['g'], data['p'], data['q'], data['x'])
            else: # only public key
                t = (data['y'], data['g'], data['p'], data['q'])
            a = Address(dsa=DSA.construct(t))
            if 'enc' in data and 'iv' in data:
                a.enc = data['enc']
                a.iv = data['iv']
            return a
        # JSON ValueError for decode
        # KeyError if no accessed key
        # DSA TypeError if not int
        except (ValueError, KeyError, TypeError):
            return None
