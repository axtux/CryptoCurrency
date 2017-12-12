import json
from Crypto.PublicKey import DSA

# local imports
from lib.utils import ripemd_160, aes

class Address(object):
    """manage DSA asymetric keys and adds some methods
    used as private and public key for the Wallet
    """
    def __init__(self, dsa=None):
        if dsa is None:
            self.dsa = DSA.generate(1024)
        else:
            self.dsa = dsa

    def __str__(self):
        """Create hash from public key to make an address
        """
        k = self.dsa
        return ripemd_160([str(k.y), str(k.g), str(k.p), str(k.q)])

    def __eq__(self, other):
        return self.toJson() == other.toJson()

    def public(self):
        return Address(self.dsa.publickey())

    def encryptPrivateKey(self, password):
        """Encrypt the private key with AES
        """
        if not self.dsa.has_private():
            return
        # encoding key as numeric string is fine
        self.enc = aes(password).encrypt(str(self.dsa.x)).hex()
        # only public key
        self.dsa = self.dsa.publickey()

    def decryptPrivateKey(self, password):
        """DEcrypt the private key with AES
        """
        if self.dsa.has_private() or self.enc is None:
            return
        # decode int from numeric string
        x = int(aes(password).decrypt(bytes.fromhex(self.enc)))
        # build private key
        d = self.dsa
        self.dsa = DSA.construct((d.y, d.g, d.p, d.q, x))
        self.enc = None

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
        except AttributeError:
            pass
        return json.dumps(data)

    @staticmethod
    def fromJson(json_dsa):
        try:
            data = json.loads(json_dsa)
            if 'x' in data: # private key
                t = (data['y'], data['g'], data['p'], data['q'], data['x'])
            else: # only public key
                t = (data['y'], data['g'], data['p'], data['q'])
            a = Address(DSA.construct(t))
            if 'enc' in data:
                a.enc = data['enc']
            return a
        # JSON ValueError for decode
        # KeyError if no accessed key
        # DSA TypeError if not int
        except (ValueError, KeyError, TypeError):
            return None
