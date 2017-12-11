from lib.address import Address

import unittest

class Test(unittest.TestCase):
    
    def equalAddresses(self, a, b):
        return a.dsa.y == b.dsa.y and a.dsa.g == b.dsa.g and a.dsa.p == b.dsa.p and a.dsa.q == b.dsa.q and a.dsa.x == b.dsa.x
    
    def test_init(self):
        a = Address()
        b = Address(a.dsa)
        self.assertTrue(self.equalAddresses(a, b))
    
    def test_json(self):
        a = Address()
        b = Address.fromJson(a.toJson())
        self.assertTrue(self.equalAddresses(a, b))
    
    def test_public_address(self):
        a = Address()
        b = a.public()
        self.assertEqual(str(a), str(b))
        self.assertNotEqual(a.toJson(), b.toJson())
