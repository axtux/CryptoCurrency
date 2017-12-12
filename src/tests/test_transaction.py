from lib.address import Address
from lib.transaction import Transaction

import unittest

class TestBlockchain(object):
    def get_amount_of_address(self, address):
        return 10

class Test(unittest.TestCase):
    
    def equalAddresses(self, a, b):
        return a.dsa.y == b.dsa.y and a.dsa.g == b.dsa.g and a.dsa.p == b.dsa.p and a.dsa.q == b.dsa.q and a.dsa.x == b.dsa.x
    
    def test_init(self):
        a = Address()
        bc = TestBlockchain()
        rs = [('lui', 2), ('elle', 3)]
        t = Transaction(a.public(), rs)
    
    def test_json_1(self):
        a = Address()
        bc = TestBlockchain()
        rs = [('lui', 2), ('elle', 3)]
        t = Transaction(a.public(), rs)
        t.toJson()
    
    def test_json_2(self):
        a = Address()
        bc = TestBlockchain()
        rs = [('lui', 2), ('elle', 3)]
        t = Transaction(a.public(), rs)
        t.sign(a)
        t2 = Transaction.fromJson(t.toJson())
        self.assertEqual(t.toJson(), t2.toJson())
    
    def test_total_amount(self):
        a = Address()
        bc = TestBlockchain()
        rs = [('lui', 2), ('elle', 3)]
        t = Transaction(a.public(), rs)
        self.assertEqual(5, t.get_total_amount())
    
    def test_not_signed(self):
        a = Address()
        bc = TestBlockchain()
        rs = [('lui', 2), ('elle', 3)]
        t = Transaction(a.public(), rs)
        self.assertFalse(t.is_signed())
    
    def test_signed(self):
        a = Address()
        bc = TestBlockchain()
        rs = [('lui', 2), ('elle', 3)]
        t = Transaction(a.public(), rs)
        t.sign(a)
        self.assertTrue(t.is_signed())
    
    def test_changed(self):
        a = Address()
        bc = TestBlockchain()
        rs = [('lui', 2), ('elle', 3)]
        t = Transaction(a.public(), rs)
        t.sign(a)
        t.receivers = [('lui', 3), ('elle', 3)]
        self.assertFalse(t.is_signed())
    
    def test_valid(self):
        a = Address()
        bc = TestBlockchain()
        rs = [('lui', 7), ('elle', 3)]
        t = Transaction(a.public(), rs)
        self.assertFalse(t.is_signed())
    
    def test_not_valid(self):
        a = Address()
        bc = TestBlockchain()
        rs = [('lui', 8), ('elle', 3)]
        t = Transaction(a.public(), rs)
        self.assertFalse(t.is_signed())
