import utils.py import sha_256
import block.py
import sqlite3 

conn = sqlite3.connect("Blockchain.db")

conn.execute("""
CREATE TABLE IF NOT EXISTS Blockchain_blocks (
    hash_of_previous_block CHAR(256) PRIMARY KEY, # pas sur exactement de quel longeur est le digest 
    transactions CHAR(50), # Je sais pas quel longeur ont les transactions
    proof_of_work INTEGER DEFAULT NULL,
    difficulty INTEGER DEFAULT NULL,
);
""")

conn.execute("""
CREATE TABLE IF NOT EXISTS Blockchain_address (
    address CHAR(256) PRIMARY KEY,
    money_of_address CHAR(50), # Je sais pas quel longeur ont les transactions
    flag BOOLEAN,
);
""")

conn.close()

class Blockchain:
	count = 0
	first_hash = sha_256("42")

	def __init__(self):
		self._last_block = Block(self.first_hash)
		self._last_hash = sha_256(str(self._last_block))

	def get_last_block(self):
		return self._last_block

	def get_last_hash(self):
		return self._last_hash

	def add_block(self, block):
		conn = sqlite3.connect("Blockchain.db")
		self._last_block = block
		self._last_hash = sha_256(str(self._last_block))
		conn.execute("INSERT INTO Blockchain_blocks (Hash_of_previous_block, Transactions, Proof_of_work, Difficulty) VALUES (block.previousHash, block.transactions, block.pow, block.difficulty)");
		for i in len(block.transactions):
			cursor.execute("""SELECT address, money_of_address, flag FROM Blochain_address WHERE address=?""", (block.transactions[i].receiver,))
			temp = cursor.fetchone()
			if type(temp) == "NoneType":
				conn.execute("INSERT INTO Blockchain_address (address, money_of_address, flag) VALUES (block.transactions[i].receiver, block.transactions[i].amount, FALSE)");
			else:
				temp_amount = temp[1] + block.transactions[i].amount
				conn.execute("UPDATE Blockchain_address set money_of_address = temp_amount where address = block.transactions[i].receiver");
			cursor.execute("""SELECT address, money_of_address, flag FROM Blochain_address WHERE address=?""", (block.transactions[i].sender,))
			temp = cursor.fetchone()
			if type(temp) == "NoneType":
				conn.execute("INSERT INTO Blockchain_address (address, money_of_address, flag) VALUES (block.transactions[i].sender, block.transactions[i].amount, TRUE)");
			else:
				temp_amount = temp[1] - block.transactions[i].amount
				conn.execute("UPDATE Blockchain_address set money_of_address = temp_amount where address = block.transactions[i].sender");
				conn.execute("UPDATE Blockchain_address set flag = TRUE where address = block.transactions[i].sender");
		conn.commit()
		conn.close()

	def get_next_block(self, hash):
		conn = sqlite3.connect("Blockchain.db")
		id = hash
		cursor.execute("""SELECT id, Transactions, Proof_of_work , Difficulty FROM users WHERE id=?""", (id,))
		response = cursor.fetchone()
		block = Block(response[0], response[1], response[2], response[3])
		conn.commit()
		conn.close()
		return block
