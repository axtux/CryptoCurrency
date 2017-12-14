import sqlite3

# local imports
from lib.utils import sha_256
from lib.block import Block
from lib.transaction import Transaction
from lib.address import Address
from lib.log import debug, warning

"""API
get_last_hash(): string
    last block hash
get_next_block(previous_hash): Block or None
    block following previous hash or None (mainly used for servers)
get_amount_of_address(address): int
    positive amount (can be 0)
is_spent(address): boolean
    return True if address has been used as source (and cannot be used again)
add_block(block): boolean
    check and add block to blockchain (also check all transactions)
    return True on success, False on error
"""

class Blockchain(object):
    """handle blocks storage and addresses amount database
    for now, this class assumes transactions are valid
    """
    FIRST_HASH = sha_256("42")
    REWARD = 10 # for each mined block

    def __init__(self, name):
        self.db = BlockchainDatabase(name)
        #print('initated BDD, last hash: '+self.get_last_hash())

    def __repr__(self):
        temp = "\n"
        hash_temp = Blockchain.FIRST_HASH
        next_block = self.get_next_block(hash_temp)
        i = 0
        while not next_block is None:
            temp += "block " + str(i) + " is \n" + str(next_block.toJson()) + "\n"
            i += 1
            hash_temp = next_block.get_hash()
            next_block = self.get_next_block(hash_temp)
        return temp + "\n"

    def get_last_hash(self):
        h = self.db.get_last_hash()
        if h is None:
            return Blockchain.FIRST_HASH
        return h

    def get_next_block(self, previous_hash):
        json = self.db.get_json_block(previous_hash)
        if json is None:
            return None
        return Block.fromJson(json[0])

    def get_amount_of_address(self, address):
        r = self.db.get_address(str(address))
        if r is None or r[2]: # r[2] is is_spent
            return 0
        return int(r[1])

    def is_spent(self, address):
        r = self.db.get_address(str(address))
        if r is None:
            return False
        return bool(r[2])

    def add_block(self, block):
        # check last hash
        if self.get_last_hash() != block.previous_hash:
            warning('last hash not matching')
            return False

        # check transactions validity
        if not block.is_valid(self):
            warning('block not valid')
            return False

        debug('accepted block')
        # add block, save THEN change last hash
        self.db.add_json_block(self.get_last_hash(), block.toJson())
        self.db.set_last_hash(block.get_hash())

        # reward sender
        self.update_addresses_amount([(block.miner_address, Blockchain.REWARD)])

        # transactions are already checked within block
        for t in block.transactions:
            sender = t.senderAddress()
            self.db.add_address(sender)
            self.db.set_address_spent(sender, True)
            self.update_addresses_amount(t.receivers)
        return True

    def update_addresses_amount(self, receivers):
        for address, amount in receivers:
            debug('updating '+str(address)+' by '+str(amount))
            tmp = self.db.get_address(address)
            if tmp is None: # do not exists
                debug('address '+str(address)+' does not exists, creating')
                self.db.add_address(address, amount)
            else:
                new_amount = int(tmp[1]) + amount
                self.db.set_address_amount(address, new_amount)


class BlockchainDatabase(object):
    def __init__(self, name):
        self.conn = sqlite3.connect("databases/"+name+".db")

        # blocks
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS blocks (
            previous_hash TEXT PRIMARY KEY NOT NULL,
            json_block TEXT NOT NULL
        );""")

        # last_hash
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS last_hash (
            void INTEGER PRIMARY KEY NOT NULL,
            hash TEXT
        );""")

        # addresses with amount and spent flag
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS addresses (
            address TEXT PRIMARY KEY NOT NULL,
            amount INTEGER DEFAULT NULL,
            spent BOOLEAN DEFAULT NULL
        );""")

    """
    def fetch_one(self, sql, params=None):
        cursor = self.conn.cursor()
        cursor.execute(sql, params)
        return cursor.fetchone()

    def fetch_all(self, sql, params=None):
        cursor = self.conn.cursor()
        cursor.execute(sql, params)
        return cursor.fetchall()

    def commit(self, sql, params=None):
        cursor = self.conn.cursor()
        cursor.execute(sql, params)
        elf.conn.commit()
        # TODO check cursor.rowcount
        return cursor.rowcount
    """

    def get_json_block(self, previous_hash):
        cursor = self.conn.cursor()
        sql = "SELECT json_block FROM blocks WHERE previous_hash=?"
        cursor.execute(sql, (previous_hash,))
        return cursor.fetchone()

    def add_json_block(self, previous_hash, json_block):
        cursor = self.conn.cursor()
        sql = "INSERT INTO blocks (previous_hash, json_block) VALUES (?, ?) ;"
        cursor.execute(sql, (previous_hash, json_block))
        self.conn.commit()

    def add_address(self, address, amount=0, spent=False):
        cursor = self.conn.cursor()
        sql = "INSERT INTO addresses (address, amount, spent) VALUES (?, ?, ?) ;"
        cursor.execute(sql, (address, amount, spent))
        self.conn.commit()

    def get_last_hash(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT hash FROM last_hash")
        res = cursor.fetchone()
        if res is None:
            return res
        else:
            return res[0]

    def get_address(self, address):
        cursor = self.conn.cursor()
        sql = "SELECT address, amount, spent FROM addresses WHERE address=? ;"
        cursor.execute(sql, (address, ))
        res = cursor.fetchone()
        return res

    def set_last_hash(self, last_hash):
        cursor = self.conn.cursor()
        if self.get_last_hash() is None:
            sql = "INSERT INTO last_hash  (void, hash) VALUES (?, ?)"
            cursor.execute(sql, (0, last_hash))
        else:
            sql = "UPDATE last_hash SET hash = ? WHERE void = 0"
            cursor.execute(sql, (last_hash,))
        self.conn.commit()

    def set_address_amount(self, address, amount):
        cursor = self.conn.cursor()
        sql = "UPDATE addresses SET amount=? WHERE address=? ;"
        cursor.execute(sql, (amount, address))
        self.conn.commit()

    def set_address_spent(self, address, spent=1):
        cursor = self.conn.cursor()
        sql = "UPDATE addresses SET spent=? WHERE address=? ;"
        cursor.execute(sql, (spent, address))
        self.conn.commit()

def print_blocks(db):
    cursor = db.conn.cursor()
    cursor.execute("SELECT * FROM blocks")
    rows = cursor.fetchall()
    for row in rows:
        print("block:")
        print(row[0])
        print(row[1])
        # with a block, call block.transactions
        transactions = []
        for transaction in transactions:
            print("transaction:")
            print(transaction[1])
            print(transaction[2])
            print(transaction[3])
            print(transaction[4])
            print("\n")
    print("finished printing the DB")


def print_addresses(db):
    cursor = db.conn.cursor()
    cursor.execute("SELECT * FROM addresses")
    rows = cursor.fetchall()
    for row in rows:
        if bool(row[2]) == False:
            temp = "This address has not been used"
        else:
            temp = "This address has been used"
        print("address " + str(row[0]) + " has amount " + str(row[1]) + ". " + temp)
    db.conn.commit()

if __name__ == '__main__':

    """
     the next lines are some tests of our functions
    """


    print("NEW TEST:\n")
    blockchain = Blockchain("blockchain")
    print("empty blockchain")
    print(blockchain)
    db = blockchain.db
    previousHash = blockchain.get_last_hash()
    print("previousHash")
    print(previousHash)

    print("TESTING Blocks DB")

    sender_address = Address()
    receiver1_address = Address()
    receiver2_address = Address()
    miner_address = Address()
    transaction = Transaction(sender_address.public(), [(str(receiver1_address), 123), (str(receiver2_address), 321)])
    print("transaction")
    print(str(transaction.toJson()))
    block = Block(previousHash, str(miner_address), [transaction])
    block.set_proof("43334")
    print("block")
    print(str(block.toJson()))
    json_block = block.toJson()
    print("json_block")
    print(str(json_block))

    db.add_json_block(previousHash, json_block)
    print("updated DB")
    print_blocks(db)

    db.set_last_hash(block.get_hash())
    previousHash2 = db.get_last_hash()

    sender2_address = Address()
    receiver21_address = Address()
    receiver22_address = Address()
    miner2_address = Address()
    transaction2 = Transaction(sender2_address.public(), [(str(receiver21_address), 321), (str(receiver22_address), 333)])
    print("transaction2")
    print(str(transaction2.toJson()))
    block2 = Block(previousHash2, str(miner2_address), [transaction2])
    block2.set_proof("222")
    print("block2")
    print(str(block2.toJson()))
    json_block2 = block2.toJson()
    print("json_block2")
    print(str(json_block2))

    db.add_json_block(previousHash2, json_block2)
    print("updated DB")
    print_blocks(db)
    db.set_last_hash(block2.get_hash())
    previousHash3 = db.get_last_hash()

    sender3_address = Address()
    receiver31_address = Address()
    receiver32_address = Address()
    miner3_address = Address()
    transaction3 = Transaction(sender3_address.public(), [(str(receiver31_address), 321), (str(receiver32_address), 333)])
    print("transaction3")
    print(str(transaction3.toJson()))
    sender4_address = Address()
    receiver41_address = Address()
    receiver42_address = Address()
    miner4_address = Address()
    transaction4 = Transaction(sender4_address.public(), [(str(receiver41_address), 321), (str(receiver42_address), 333)])
    print("transaction4")
    print(str(transaction4.toJson()))

    block3 = Block(previousHash3, str(miner3_address), [transaction3, transaction4])
    block3.set_proof("222")
    print("block3")
    print(str(block3.toJson()))
    json_block3 = block3.toJson()
    print("json_block3")
    print(str(json_block3))

    db.add_json_block(previousHash3, json_block3)
    print("updated DB")
    print_blocks(db)
    db.set_last_hash(block3.get_hash())
    previousHash4 = db.get_last_hash()

    print("getting block")
    print(db.get_json_block(previousHash2))
    print("compared to")
    print(json_block2)

    print("\n,\n,\n,\n")

    print("TESTING ADDRESS DB")
    print("printing adress DB")
    print_addresses(db)

    db.add_address(str(sender_address), 0, 1)
    db.add_address(str(receiver1_address), 123, 0)
    db.add_address(str(receiver2_address), 321,0)
    print("printing address DB after havin added")
    print_addresses(db)
    db.set_address_amount(str(sender_address), 100)
    print("printing address DB after modification")
    print_addresses(db)
    db.set_address_spent(str(sender_address), 0)
    print("printing address DB after modification")
    print_addresses(db)
    print("getting address")
    print(db.get_address(str(receiver1_address)))



    conn = sqlite3.connect("databases.blockchain.db")
    cursor = conn.cursor()
    print("deleting DB")
    cursor.execute("""
        DROP TABLE blocks
    """)
    cursor.execute("""
        DROP TABLE addresses
    """)
    cursor.execute("""
        DROP TABLE last_hash
    """)
    conn.commit()
    print("destroyed")

    print("\n,\n,\n,\n")


    print("TESTING BLOCKCHAIN:\n")
    blockchain = Blockchain("blockchain")
    print("empty blockchain")
    print(blockchain)
    db = blockchain.db
    previousHash = blockchain.get_last_hash()
    print("previousHash")
    print(previousHash)

    print("block that is being added")
    print(str(block.toJson()))
    blockchain.add_block(block)
    print("updated blockchain")
    print(blockchain)
    print("updated addresses DB")
    print_addresses(db)
    print("updated blocks DB")
    print_blocks(db)
    print("getting last hash")
    print(blockchain.get_last_hash())
    print("block that is being added")
    print(str(block2.toJson()))
    blockchain.add_block(block2)
    print("updated blockchain")
    print(blockchain)
    print("updated addresses DB")
    print_addresses(db)
    print("updated blocks DB")
    print_blocks(db)
    print("getting last hash")
    print(blockchain.get_last_hash())
    print("block that is being added")
    print(str(block3.toJson()))
    blockchain.add_block(block3)
    print("updated blockchain")
    print(blockchain)
    print("updated addresses DB")
    print_addresses(db)
    print("updated blocks DB")
    print_blocks(db)
    print("getting last hash")
    print(blockchain.get_last_hash())


    conn = sqlite3.connect("databases.blockchain.db")
    cursor = conn.cursor()
    print("deleting DB")
    cursor.execute("""
        DROP TABLE blocks
    """)
    cursor.execute("""
        DROP TABLE addresses
    """)
    cursor.execute("""
        DROP TABLE last_hash
    """)
    conn.commit()
    print("destroyed")
    

    # we detroy the data base once we have destroyed the block chain
