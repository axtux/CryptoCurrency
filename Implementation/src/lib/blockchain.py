import sqlite3

# local imports
from lib.utils import sha_256
from lib.block import Block
from lib.transaction import Transaction
from lib.address import Address

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

    def __init__(self):
        self.db = BlockchainDatabase("blockchain")
        #print('initated BDD, last hash: '+self.get_last_hash())

    def __repr__(self):
        temp = "\n"
        hash_temp = Blockchain.FIRST_HASH
        next_block = self.get_next_block(hash_temp)
        while next_block != None:
            temp += "block " + str(i) + " is \n" + str(next_block) + "\n"
            i += 1
            hash_temp = next_block.get_hash()
        return temp + "\n"

    def get_last_hash(self):
        h = self.db.get_last_hash()
        if h == None:
            return Blockchain.FIRST_HASH
        return h

    def get_next_block(self, previous_hash):
        json = self.db.get_json_block(previous_hash)
        if json == None:
            return None
        return Block.fromJson(json)

    def get_amount_of_address(self, address):
        r = self.db.get_address(address)
        if r == None or r[2]: # r[2] is is_spent
            return 0
        return int(r[1])

    def is_spent(self, address):
        r = self.db.get_address(address)
        if r == None:
            return False
        return bool(r[2])

    def add_block(self, block):
        # check transactions validity
        if not block.is_valid(self):
            return False

        # add block
        self.db.set_last_hash(block.get_hash())
        self.db.add_json_block(self.db.get_last_hash(), block.toJson())

        # transactions are already checked within block
        for t in block.transactions:
            sender = t.senderAddress()
            self.db.set_address_spent(sender, True)
            self.update_addresses_amount(t.receivers)
        return True

    def update_addresses_amount(self, receivers):
        for address, amount in receivers:
            tmp = self.db.get_address(address)
            if tmp == None: # do not exists
                self.db.set_address_amount(address, amount, False)
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
        sql = "SELECT previous_hash, json_block FROM blocks WHERE previous_hash=?"
        cursor.execute(sql, (previous_hash,))
        return cursor.fetchone()

    def add_json_block(self, previous_hash, json_block):
        cursor = self.conn.cursor()
        sql = "INSERT INTO blocks (previous_hash, json_block) VALUES (?, ?) ;"
        cursor.execute(sql, (previous_hash, json_block))
        self.conn.commit()

    def add_address(self, address, amount=0, spent=0):
        cursor = self.conn.cursor()
        sql = "INSERT INTO addresses (address, amount, spent) VALUES (?, ?, ?) ;"
        cursor.execute(sql, (address, amount, spent))
        self.conn.commit()

    def get_last_hash(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT hash FROM last_hash")
        res = cursor.fetchone()
        if res == None:
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
        if self.get_last_hash() == None:
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

    print("NEW TEST:\n")
    blockchain = Blockchain()
    db = blockchain.db
    previousHash = blockchain.get_last_hash()


    print("TESTING Blocks DB")

    blockchain = Blockchain()
    db = blockchain.db
    previousHash = blockchain.get_last_hash()

    sender = Address()
    receiver1 = Address()
    receiver2 = Address()
    transactions = [Transaction(sender.public(), ([str(receiver1), str(receiver2)], [123, 321]))]
    #iv = iv()
    miner_address = Address()
    block = Block(previousHash, str(miner_address), transactions)
    block.set_proof("43334")
    json_block = block.toJson()

    db.add_json_block(previousHash, json_block)
    print("DB with block added")
    print_blocks(db)

    """
    db.fetch_one()
    db.fetch_all()
    db.commit()
    """
    db.get_json_block(previousHash)
    print("get_last_hash")
    print(db.get_last_hash())

    print("TESTING ADDRESS DB")
    print("printing adress DB")
    print_addresses(db)

    db.add_address(str(sender), 0, 1)
    db.add_address(str(receiver1), 123, 0)
    db.add_address(str(receiver2), 321,0)
    print("printing address DB after havin added")
    print_addresses(db)
    db.set_address_amount(str(sender), 100)
    print("printing address DB after modification")
    print_addresses(db)
    db.set_address_spent(str(sender), 0)
    print("printing address DB after modification")
    print_addresses(db)




    print("TESTING LAST_HASH DB")
    db.set_last_hash(sha_256("42"))
    print(db.get_last_hash())
    db.set_last_hash(sha_256("4"))
    print(db.get_last_hash())


    """
    db.set_last_hash(sha_256("2"))
    print(db.get_last_hash())
    """



    print("\n\n\n\n\n")

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

    blockchain = Blockchain()

    print("passed2")
    blockchain.add_block(block)
    print("passed3")
    print("printing blockchain\n" + str(blockchain))
    print("printing address list")
    print_addresses(db)
    print("finished printing address list")




    print("\n\n\n\n\n")
    previousHash = blockchain.get_last_hash()
    transaction_1 = Transaction(322, "A", "B")
    transaction_2 = Transaction(234324, "Z", "T")
    transactions = [transaction_1, transaction_2]
    block2 = Block(previousHash, transactions)

    blockchain.add_block(block2)
    print(blockchain)
    print("printing adresses")
    print_addresses(db)

    print(blockchain.get_amount_of_address("A"))
    print(blockchain.get_last_hash())
    print(sha_256(str(block2)))

    # we detroy the data base once we have destroyed the block chain
