import sys
import getpass

# local imports
import lib.walletDB as db
from lib.address import Address
from lib.blockchain import Blockchain
from lib.http_client import RelayClient
from lib.updater import Updater
from lib.transaction import Transaction

def display_addresses(bc):
    addresses = db.loadAddressList('client')
    for addr in addresses:
        if bc.is_spent(addr):
            status = 'spent'
        else:
            status = bc.get_amount_of_address(addr)
        print(str(addr)+': '+str(status))

def create_address():
    pwd = getpass.getpass()
    addr = Address()
    addr.encryptPrivateKey(pwd)
    db.add_address('client', addr, 0)
    print('created new address '+str(addr))

def get_address(address):
    ads = db.loadAddressList('client')
    for a in ads:
        if str(a) == str(address):
            return a

def transfer(bc, relay, from_addr, to_addr, amount):
    f = get_address(from_addr)
    if f is None:
        exit('no address '+str(from_addr)+' in database')
    
    total = bc.get_amount_of_address(f)
    if total < amount:
        exit('not enough money for this transfer')
    
    pwd = getpass.getpass()
    # TODO: check bad pwd
    f.decryptPrivateKey(pwd)
    
    receivers = [(to_addr, amount)]
    if total > amount:
        print('creating new address for remaining funds')
        new = Address()
        new.encryptPrivateKey(pwd)
        receivers.append((str(new), total - amount))
    else:
        new = None
    t = Transaction(f, receivers)
    if relay.submit_transaction(t):
        if new is None:
            print('transaction sent to the network')
        else:
            db.add_address('client', new, 0)
            print('transaction sent to the network, your new address is '+str(new))
    else:
        print('error sending transaction')


def usage():
    exit('usage: python3 '+av[0]+' list|new|transfer')

if __name__ == '__main__':
    # init database
    db.createDB()
    
    # always update blockchain
    bc = Blockchain('client')
    relay = RelayClient()
    u = Updater(bc, relay)
    print('updating blockchain')
    u.update()
    
    # parse arguments
    av = sys.argv
    ac = len(av)
    if ac == 1:
        usage()
    
    if av[1] == 'list':
        display_addresses(bc)
    elif av[1] == 'new':
        create_address()
    elif av[1] == 'transfer':
        try:
            transfer(bc, relay, av[2], av[3], int(av[4]))
        except (IndexError, ValueError): # not enough args or AMOUNT not int
            exit('usage: python3 '+av[0]+' transfer FROM_ADDR TO_ADDR AMOUNT')
    else:
        usage()
