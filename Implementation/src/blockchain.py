import utils.py
import block.py
import mysql.connector 

conn = mysql.connector.connect(host="localhost",user="root",password="XXX", database="Blockchain_blocks")
cursor = conn.cursor()
conn.close()
# Pas sur de ce que je fais, DB et server ça me connais pas

cursor.execute("""
CREATE TABLE IF NOT EXISTS Blockchain_blocks (
    Hash_of_previous_block varchar(256) DEFAULT NULL, # pas sur exactement de quel longeur est le digest 
    Transactions varchar(50) DEFAULT NULL, # Je sais pas quel longeur ont les transactions
    Proof_of_work INTEGER DEFAULT NULL,
    Difficulty INTEGER DEFAULT NULL,
    PRIMARY KEY(Hash_of_previous_block)
);
""")

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
		self._last_block = block
		self._last_hash = sha_256(str(self._last_block))
		block_temp = {"Hash_of_previous_block": str(block.previousHash), "Transactions" : str(block.transactions), "Proof_of_work" : block.pow, "Difficulty" : block.difficulty}
		cursor.execute("""INSERT INTO Blockchain_blocks (Hash_of_previous_block, Transactions, Proof_of_work, Difficulty) VALUES(%(Hash_of_previous_block)s, %(Transactions)s, %(Proof_of_work)s, %(Difficulty)s)""", block_temp)

	def get_next_block(self, hash)
		id = hash
		cursor.execute("""SELECT id, Transactions, Proof_of_work , Difficulty FROM users WHERE id=?""", (id,))
		response = cursor.fetchone()
		block = Block(response[0], response[1], response[2], response[3])
		return block