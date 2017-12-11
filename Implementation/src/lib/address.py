import json
from Crypto.PublicKey import DSA

# local imports
from lib.utils import ripemd_160

class Address(object):
    """manage DSA asymetric keys and adds some methods
    used as private and public key for the Wallet
    """
    def __init__(self, dsa=None):
        if dsa is None:
            self.dsa = DSA.generate(1024)
        else:
            self.dsa = dsa
        """TODO move to BDD
        if addr == None:    #Generate  a new address
            self.iv = iv()
            self.privateKey = generateDSAKey()
            self.privateKey.x = encrypt_AES(AES_Key, intToBytes(self.privateKey.x), self.iv)
            self.publicKey = self.privateKey.publickey()
            self.address = self.generateAddress()
            recordAddress(self.address, self.publicKey.y, self.publicKey.g, self.publicKey.p, self.publicKey.q, self.privateKey.x, self.iv)
        else:   #Load an existing address
            self.address = addr
            self.privateKey, self.iv = loadKey(self.address)
            self.publicKey = self.privateKey.publickey()
        """

    def __str__(self):
        """Create hash from public key to make an address
        """
        k = self.dsa
        return ripemd_160([str(k.y), str(k.g), str(k.p), str(k.q)])
    
    def public(self):
        return Address(self.dsa.publickey())
    
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
        return json.dumps(data)
    
    @staticmethod
    def fromJson(json_dsa):
        try:
            data = json.loads(json_dsa)
            if ('x' in data): # private key
                t = (data['y'], data['g'], data['p'], data['q'], data['x'])
            else: # only public key
                t = (data['y'], data['g'], data['p'], data['q'])
            return Address(DSA.construct(t))
        # JSON ValueError for decode
        # KeyError if no accessed key
        # DSA TypeError if not int
        except (ValueError, KeyError, TypeError):
            return None
