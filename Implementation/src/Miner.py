import utils.py
"""import l'interface contenant toutes les methodes cryptographics"""
import itertools
""" import d'outil pour générer toutes les permutations d'une liste """


class Miner:

	""" A Miner gives the proof of work to give the first step of confirmation for a transaction
    Miners contain
     - the list of the transactions on which there working
     - flag to show that they are working
     - amount of money they own
    They can
     - request transactions
     - mine them
     - send packages of transactions to relmay nodes once they'r good enough"""

	def __init__(self):
		self._transactions = []
		self._mining = 0
		"flag to show that they are mining and must not be sent transactions"
		self._money = 0


	def hashTransactions(self, start = 0, stop = len(_transactions)):
		""" Methodes recursives qui hash les transactions """
		if stop - start == 0:
			return hash(_transactions[start]);
		else:
			hash1 = self.hashTransactions(start, start + (stop-start)//2);
			hash2 = self.hashTransactions(start + (stop-start)//2 + 1, stop);
 			return hash(hash1 + hash2);


 	def mine(self)
 		""" Je sais pas comment faire mais ce serrait bien d'avoir la possibilité d'interrompre le mining avec un certain bouton car ça peut pottentiellement durer très longtemps.
		Si les relay nodes n'ont pas de transaction à donner, le miner restera bloqué dans cette fonction """
		self._flag = 1
 		foundCombination = (self.hashTransactions() >= difficulty)
 		while foundCombination == false:
 			permutation = list(itertools.permutations(self._transactions))
 			i = 1
 			while i < len(permutation):
 				self._transactions = permutation[i]
 				if self.hashTransactions() < difficulty:
 					break
 				i += 1
 			if i < len(permutation):
 				break
 			if len(self._transactions > 20):
 				"sinon calculer les permutation devient trop longs"
 				self._transactions = []
 			self.requestTransactions()
 			foundCombination = (self.hashTransactions() >= difficulty)

	def submitTransactions():
		""" Donne les transactions dans l'ordre qui donne une bonnne valeur à un relay Node"""
