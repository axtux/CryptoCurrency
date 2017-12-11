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
        print('initated BDD, last hash: '+self.get_last_hash())

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
            return self.FIRST_HASH

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
        # TODO: english comments
        # On update le dernier block et le hash du dernier bloc
        # on rajoute le bloc dans la DB contenant tout les blocs
        self.db.set_last_hash(sha_256(block))
        self.db.add_json_block(blockchain.db.get_last_hash(), block.toJson())
        for i in range(len(block.transactions)):
            # Pour chaque transaction, on la rajoute dans la DB des transactions
            self.write_in_transactions_DB(block.previousHash, i, block.transactions[i].amount, block.transactions[i].sender, block.transactions[i].receiver);
            temp = self.get_address(block.transactions[i].receiver)
            if temp == None:
                # On cherche si l'addresse a deja ete utilise pour recevoir. Si non on la rajoute
                self.write_in_address_DB(block.transactions[i].receiver, block.transactions[i].amount, False);
            else:
                # Si oui on update son argent
                temp_amount = int(temp[1]) + block.transactions[i].amount
                self.db.set_address_amount(block.transactions[i].receiver, temp_amount)
            temp = self.select_address(block.transactions[i].sender)
            if temp == None:
                # On cherche si l'addresse d'envoi existe deja. Si non on la rajoute et on met le bon flag
                self.db.add_address(block.transactions[i].sender, block.transactions[i].amount, True);
            else:
                # Si oui, on update la valeur et on met le bon flag
                temp_amount = int(temp[1]) - block.transactions[i].amount
                self.db.set_address_amount(block.transactions[i].sender, temp_amount)
                self.db.set_address_spent(block.transactions[i].sender, True)
        self.db.set_last_hash(block.hash())


class BlockchainDatabase(object):
    def __init__(self, name):
        self.conn = sqlite3.connect("databases."+name+".db")
        
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
        self.cursor.execute(sql, (address))
        return self.cursor.fetchone()

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
    print("finished printingDB")


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

    password = "veryGoodPassword"
    key = sha_256(password)[:32].encode('utf-8')
    mess = "bonjour"
    #iv = iv()
    password2 = "notSoVeryGoodPassword"
    key2 = sha_256(password2)[:32].encode('utf-8')
    mess2 = "bonjour2"
    #iv = iv()
    password3 = "notSoVeryGoodPassword"
    key3 = sha_256(password2)[:32].encode('utf-8')
    mess3 = "bonjour3"
    #iv = iv()
    sender = Address(AES_Key=key)
    receiver1 = Address(AES_Key=key2)
    receiver2 = Address(AES_Key=key3)
    transactions = [Transaction(sender.publicKey, [receiver1.address, receiver2.address], [123, 321])]
    miner_pasword = "veryGoodPassword"
    key_miner = sha_256(password)[:32].encode('utf-8')
    mess_miner = "bonjour"
    #iv = iv()
    miner_address = Address(AES_Key=key_miner)
    block = Block(previousHash, miner_address.address, transactions)
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

    db.add_address(sender.address, 0, 1)
    db.add_address(receiver1.address, 123, 0)
    db.add_address(receiver2.address, 321,0)
    print("printing address DB after havin added")
    print_addresses(db)
    db.set_address_amount(sender.address, 100)
    print("printing address DB after modification")
    print_addresses(db)
    db.set_address_spent(sender.address, 0)
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

    
    # On detruit la base de donnee un fois qu'on detruit la blockchain
    
