from lib.address import Address

import unittest

class Test(unittest.TestCase):
    
    def equalAddresses(self, a, b, x=True, enc=False):
        if x and a.dsa.x != b.dsa.x:
            return False
        if enc and a.enc != b.enc:
            return False
        return a.dsa.y == b.dsa.y and a.dsa.g == b.dsa.g and a.dsa.p == b.dsa.p and a.dsa.q == b.dsa.q
    
    def test_init(self):
        a = Address()
        b = Address(a.dsa)
        self.assertTrue(self.equalAddresses(a, b))
    
    def test_encrypted(self):
        a = Address()
        b = Address(a.dsa)
        b.encryptPrivateKey('pwd')
        b.decryptPrivateKey('pwd')
        self.assertTrue(self.equalAddresses(a, b))
    
    def test_json(self):
        a = Address()
        b = Address.fromJson(a.toJson())
        self.assertTrue(self.equalAddresses(a, b))
        
    def test_encrypted_json(self):
        a = Address()
        a.encryptPrivateKey('pwd')
        b = Address.fromJson(a.toJson())
        self.assertTrue(self.equalAddresses(a, b, False, True))
    
    def test_public_json(self):
        a = Address().public()
        b = Address.fromJson(a.toJson())
        self.assertTrue(self.equalAddresses(a, b, False))
    
    def test_public_address(self):
        a = Address()
        b = a.public()
        self.assertEqual(str(a), str(b))
        self.assertNotEqual(a.toJson(), b.toJson())
