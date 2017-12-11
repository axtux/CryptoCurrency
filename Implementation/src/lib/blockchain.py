import sqlite3 

# local imports
from lib.utils import sha_256
from lib.block import Block
from lib.transaction import Transaction
from lib.address import Address
from lib.miner import Miner

class Blockchain(object):
    """handle blocks storage and addresses amount database
    for now, this class assumes transactions are valid
    """
    FIRST_HASH = sha_256("42")

    def __init__(self):
        self.db = BlockchainDatabase("blockchain")
        self.last_hash = self.get_last_hash()
        if self.last_hash == None:
            self.last_hash = FIRST_HASH
        print('last hash: '+self.last_hash)

    def __repr__(self):
        temp = "\n"
        hash_temp = Blockchain.FIRST_HASH
        next_block = self.get_next_block(hash_temp)
        while next_block != None:
            temp += "block " + str(i) + " is \n" + str(next_block) + "\n"
            i += 1
            hash_temp = next_block.get_hash()
        return temp + "\n"

    def get_last_block(self):
        return self._last_block

    def get_last_hash(self):
        hash_ = self.FIRST_HASH
        block = self.get_next_block(hash_)
        while block != None:
            hash_ = sha_256(block)
            block = self.get_next_block(hash_)
        return hash_

    def get_amount_of_address(self, address):
        r = self.db.get_address(address)
        # TODO: handle if not exists
        return int(r[1])

    def add_block(self, block):
        # On update le dernier block et le hash du dernier bloc
        self.last_hash = sha_256(str(block))
        # on rajoute le bloc dans la DB contenant tout les blocs
        self.db.add_block(blockchain.last_hash, block)
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


    def get_next_block(self, previous_hash):
        json = self.db.get_block(previous_hash)
        block = Block.fromJson(json)
        return block

class BlockchainDatabase(object):
    def __init__(self, name):
        self.conn = sqlite3.connect("databases."+name+".db")
        
        # blocks
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS blocks (
            previous_hash TEXT PRIMARY KEY NOT NULL,
            json_block TEXT NOT NULL
        );""")

        # addresses with amount and spent flag
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS addresses (
            address TEXT PRIMARY KEY NOT NULL,
            amount INTEGER DEFAULT NULL,
            spent BOOLEAN DEFAULT NULL
        );""")
    
    def add_block(self, previous_hash, block):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO blocks (previous_hash, json_block) VALUES (?, ?)", (previous_hash, block.toJson()));
        self.conn.commit()
    
    def add_address(self, address, amount=0, spent=0):
        cursor = self.conn.cursor()
        sql = "INSERT INTO addresses (address, amount, spent) VALUES (?, ?) ;"
        cursor.execute(sql, (address, amount, spent))
        self.conn.commit()

    def get_block(self, previous_hash):
        cursor = self.conn.cursor()
        cursor.execute("SELECT previous_hash, json_block FROM blocks WHERE previous_hash=?", (previous_hash, ))
        json = cursor.fetchone()
        return Block.fromJson(json)

    def get_address(self, address):
        cursor = self.conn.cursor()
        sql = "SELECT address, amount, spent FROM addresses WHERE address=? ;"
        self.cursor.execute(sql, (address))
        return self.cursor.fetchone()

    def set_address_amount(self, address, amount):
        cursor = self.conn.cursor()
        sql = "UPDATE addresses SET amount=? WHERE address=? ;"
        self.cursor.execute(sql, (amount, address))
        self.conn.commit()

    def set_address_spent(self, address, spent=1):
        cursor = self.conn.cursor()
        sql = "UPDATE addresses SET spent=? WHERE address=? ;"
        self.cursor.execute(sql, (spent, address))
        self.conn.commit()

def print_blocks(db):
    cursor = db.conn.cursor()
    cursor.execute("SELECT * FROM blocks")
    rows = cursor.fetchall()
    for row in rows:
        print("block:")
        print(row[0])
        print(row[1])
        print(row[2])
        # with a block, call block.transactions
        transactions = []
        for transaction in transactions:
            print("transaction:")
            print(transaction[1])
            print(transaction[2])
            print(transaction[3])
            print(transaction[4])
            print("\n")

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
    blockchain.conn.commit()

if __name__ == '__main__':
    db = BlockchainDatabase("blocks")
    print_blocks(db)
    print("NEW TEST:\n")
    blockchain = Blockchain()
    print("passed1")
    previousHash = blockchain.get_last_hash()
    print(previousHash)
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
    miner = Miner(blockchain, miner_address, relay)
    block = Block(previousHash, miner_address.address, transactions)
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
    print("destroying de DB")
    self.cursor.execute("""
        DROP TABLE Blockchain_blocks
    """)
    self.cursor.execute("""
        DROP TABLE Blockchain_address
    """)
    self.conn.execute("""
        DROP TABLE Blockchain_transactions
    """)
    self.conn.commit()
    print("destroyed")
