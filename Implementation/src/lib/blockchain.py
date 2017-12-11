from utils import sha_256
from block import Block
from transaction import Transaction
import sqlite3 


""" Toutes cette classe se base sur le fait que toutes les transactions que l'on veut faire sont effectivement correcte.
Je peut rajouter un controle en plus si il faut"""

class Blockchain(object):
    count = 0
    first_hash = sha_256("42")

    def __init__(self):
        self.conn = sqlite3.connect("Blockchain.db")
        self.cursor = self.conn.cursor()
        # On cree une DB avec les Blocs
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS Blockchain_blocks (
            hash_of_previous_block TEXT PRIMARY KEY DEFAULT NULL,
            proof_of_work INTEGER DEFAULT NULL,
            difficulty INTEGER DEFAULT NULL
        );""")

        # On cree une DB avec les transactions qui appartiennent a chaque bloc comme dans SQLite on ne peut avoir des valeurs qui sont des listes
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS Blockchain_transactions(
            hash_of_previous_block TEXT DEFAULT NULL,
            id INTEGER DEFAULT NULL,
            amount INTEGER DEFAULT NULL,
            sender TEXT DEFAULT NULL,
            receiver TEXT DEFAULT NULL,
            PRIMARY KEY (hash_of_previous_block, id)
        );""")

        # On cree la DB avec les adresses et l'argent du compte
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS Blockchain_address (
            address TEXT PRIMARY KEY DEFAULT NULL,
            money_of_address TEXT DEFAULT NULL,
            flag BOOLEAN DEFAULT NULL
        );""")
        if Blockchain.count == 0:
            #self._last_block = Block(self.first_hash)
            #self.add_block(self._last_block)
            #self._last_hash = sha_256(str(self._last_block))
            self._last_hash = self.first_hash
        print("Finished initialising blockchain\n")

    def __repr__(self):
        # On represente les blocs en partant du bloc 0
        counter = Blockchain.count
        i = 0
        temp = "\n"
        hash_temp = Blockchain.first_hash
        while counter != 0:
            next_block = self.get_next_block(hash_temp)
            temp += "block " + str(i) + " is \n" + str(next_block) + "\n"
            i += 1
            counter -= 1
            hash_temp = sha_256(str(next_block))
        return temp + "\n"

    def write_in_blocks_DB(self, previousHash, proof_of_work, difficulty):
        self.cursor.execute("INSERT INTO Blockchain_blocks (hash_of_previous_block, proof_of_work, difficulty) VALUES (?, ?, ?)", (previousHash, proof_of_work, difficulty));
        self.conn.commit()

    def write_in_address_DB(self, address, money_of_address, flag):
        self.cursor.execute("INSERT INTO Blockchain_address (address, money_of_address, flag) VALUES (?, ?, ?)", (address, money_of_address, flag));
        self.conn.commit()

    def write_in_transactions_DB(self, previousHash, index, amount, sender, receiver):
        self.cursor.execute("INSERT INTO Blockchain_transactions (hash_of_previous_block, id, amount, sender, receiver) VALUES (?, ?, ?, ?, ?)", (previousHash, index, amount, sender, receiver));
        self.conn.commit()

    def select_address(self, address):
        self.cursor.execute("SELECT address, money_of_address, flag FROM Blockchain_address WHERE address=?", (address))
        return self.cursor.fetchone()

    def get_last_block(self):
        return self._last_block

    def get_last_hash(self):
        return self._last_hash

    def get_amount_of_address(self, address):
        self.cursor.execute("SELECT money_of_address FROM Blockchain_address WHERE address = ?", (address))
        amount = self.cursor.fetchone()
        self.conn.commit()
        return int(amount[0])

    def add_block(self, block):
        Blockchain.count += 1
        # On update le dernier block et le hash du dernier bloc
        self._last_block = block
        self._last_hash = sha_256(str(self._last_block))
        # on rajoute le bloc dans la DB contenant tout les blocs
        self.write_in_blocks_DB(block.previousHash, block.pow, block.difficulty)
        for i in range(len(block.transactions)):
            # Pour chaque transaction, on la rajoute dans la DB des transactions
            self.write_in_transactions_DB(block.previousHash, i, block.transactions[i].amount, block.transactions[i].sender, block.transactions[i].receiver);
            temp = self.select_address(block.transactions[i].receiver)
            if temp == None:
                # On cherche si l'addresse a deja ete utilise pour recevoir. Si non on la rajoute
                self.write_in_address_DB(block.transactions[i].receiver, block.transactions[i].amount, False);
            else:
                # Si oui on update son argent
                temp_amount = int(temp[1]) + block.transactions[i].amount
                self.cursor.execute("UPDATE Blockchain_address SET money_of_address = ? WHERE address = ?", (temp_amount, block.transactions[i].receiver))
            temp = self.select_address(block.transactions[i].sender)
            if temp == None:
                # On cherche si l'addresse d'envoi existe deja. Si non on la rajoute et on met le bon flag
                self.write_in_address_DB(block.transactions[i].sender, block.transactions[i].amount, True);
            else:
                # Si oui, on update la valeur et on met le bon flag
                temp_amount = int(temp[1]) - block.transactions[i].amount
                self.cursor.execute("UPDATE Blockchain_address SET money_of_address = ? WHERE address = ?", (temp_amount, block.transactions[i].sender))
                self.cursor.execute("UPDATE Blockchain_address SET flag = ? where address = ?", (True, block.transactions[i].sender));
        self.conn.commit()

    def get_next_block(self, hash_):
        identifier = hash_
        # On extrait les donnees du bloc qui sont dans la DB avec les blocs
        self.cursor.execute("SELECT hash_of_previous_block, id , amount, sender, receiver FROM Blockchain_transactions WHERE hash_of_previous_block=?", (identifier,))
        transactions = self.cursor.fetchall()
        transactions_list = []
        # Pour chaque bloc on extrait les transactions dans la DB des transactions
        for transaction in transactions:
            transaction = Transaction(transaction[2], transaction[3], transaction[4])
            transactions_list.append(transaction)
        self.cursor.execute("SELECT hash_of_previous_block, proof_of_work , difficulty FROM Blockchain_blocks WHERE hash_of_previous_block=?", (identifier,))
        response = self.cursor.fetchone()
        # On recree le bloc et on l'envoi
        block = Block(response[0], transactions_list, response[1], response[2])
        self.conn.commit()
        return block

def print_Blockchain_blocks():
    self.cursor.execute("SELECT hash_of_previous_block, proof_of_work , difficulty FROM Blockchain_blocks")
    rows = self.cursor.fetchall()
    for row in rows:
        print("block:")
        print(row[0])
        print(row[1])
        print(row[2])
        self.cursor.execute("SELECT hash_of_previous_block, id , amount , sender, receiver FROM Blockchain_transactions WHERE hash_of_previous_block=?", (row[0],))
        transactions = self.cursor.fetchall()
        for transaction in transactions:
            print("transaction:")
            print(transaction[1])
            print(transaction[2])
            print(transaction[3])
            print(transaction[4])
            print("\n")
    self.conn.commit()

def print_Blockchain_address(blockchain):
    blockchain.cursor.execute("SELECT address, money_of_address , flag FROM Blockchain_address")
    rows = blockchain.cursor.fetchall()
    for row in rows:
        if bool(row[2]) == False:
            temp = "This address has not been used"
        else:
            temp = "This address has been used"
        print("address " + str(row[0]) + " has amount " + str(row[1]) + ". " + temp)
    blockchain.conn.commit()

if __name__ == '__main__':
    
    print("NEW TEST:\n")
    blockchain = Blockchain()
    previousHash = blockchain.get_last_hash()
    transaction_1 = Transaction(123, "A", "B")
    transaction_2 = Transaction(234324, "Z", "T")
    transactions = [transaction_1, transaction_2]
    block = Block(previousHash, transactions)
    blockchain.add_block(block)
    print("printing blockchain\n" + str(blockchain))
    print("printing address list")
    print_Blockchain_address(blockchain)
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
    print_Blockchain_address(blockchain)

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
