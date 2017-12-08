#!/usr/bin/env python 
from http.server import BaseHTTPRequestHandler, HTTPServer
import requests
import json

from ..transaction import Transaction
from ..block import Block

MY_IP= '127.0.1.1'
MASTER_URL = 'http://127.0.20.1:8081'

""" 
	MAN
		for wallet 
			to implement:  (see pre/post cond.)
				getTransaction(ID)
				processTransaction(transaction)
		for miner
			to implement:  (see pre/post cond.)
				getBlock()
				processBlock(block)



"""

### TO IMPLEMENT
"""
	input: ID of the transaction
	ouput: array with ID and transaction object
"""
def getTransaction(ID):
	transaction = Transaction("moi",42,"toi")
	return (ID,transaction)

"""
	input: transaction object
	ouput: ID of the new transaction
"""
def processTransaction(transaction):
	return 42

"""
	input: none
	ouput: Block to mine
"""
def getBlock():
	return Block()

"""
	input: a block object
	ouput: True if ok, False else
"""
def processBlock(block):
	return True



### INTERNAT STUFF ##



# Obtain a copy of the blockchain
def getBlockchain():
	data = False
	r = requests.get(MASTER_URL+"/blockchain")
	
	if r.status_code==200:
		return r.text
	else:
		raise Exception

	 
	 
# submit a block
	

def submitBlockchain(data):
	data = False
	r = requests.post(MASTER_URL+"/blockchain/",data=data)
	
	if r.status_code==200:
		return r.text
	else:
		raise Exception


 
# HTTPRequestHandler class
class testHTTPServer_RequestHandler(BaseHTTPRequestHandler):
	def getTransactionResponse(self,id):
		return getTransaction()
	def postTransactionResponse(self,data):
		return processTransaction(Transaction(**data))
	
	def getWorkResponse(self):
		return getBlock()
		
	def submitWorkResponse(self,data):
		return processBlock(Block(**data))
 
	# GET
	def do_GET(self):
		try:
			resp=""
			if self.path.startswith("/transaction/"):
				id = 5 #parse id
				resp = self.getTransactionResponse(id)
			elif self.path == "/getWork" :
				resp = self.getWorkResponse()        
			else:        
				self.send_error(404, str(self.path)+" not found")
				return

			self.send_header('Content-type','text/json')
			self.end_headers()

			print(resp)
	 
			self.wfile.write(bytes(str(resp), "utf8"))
			return 
		except Exception as e:
			self.send_error(500, str(e))
			raise e
		
		
	# POST
	def do_POST(self):
		try:
			resp=""			
			data = json.loads(self.rfile.read(int(self.headers['Content-Length'])).decode("utf-8") )
			if self.path == "/transaction/":
				resp = self.postTransactionResponse(json)
			elif self.path == "/submitBlock" :
				resp = self.submitWorkResponse(json)        
			else:        
				self.send_error(404, str(self.path)+" not found")
				return

			self.send_header('Content-type','text/json')
			self.end_headers()
	 
			self.wfile.write(bytes(str(resp), "utf8"))
			return
		except Exception as e:
			self.send_error(500, str(e))

 
def run():
	print('starting server...')
 
	server_address = (MY_IP, 8081)
	httpd = HTTPServer(server_address, testHTTPServer_RequestHandler)
	print('running server...')
	httpd.serve_forever()
 
 
run()



def doTEST():





"""
	protocol spec as server
	 ask for a transaction
		GET /transaction/ID
			Response code 200 : a json list with
					{
					 ID: block id,
					 DATA: data,
					 Hash: hash of the block   
					}
	 make a transaction
		POST /transaction
			 Response code 200 : a json list with
					{
					 ..
					},

	protocol spec as server (from miner to relay)     
	 ask for a block       
		GET /getWork
			Response code 200 : a json list with
					{
					 ID: block id,
					 DATA: data, 
					}
	 
	 submit a block
		POST /submitBlock
			 Response code 200 : a json list with
					{
					 ID: block id,
					 DATA: data, 
					 HASH: proof of work
					}

	protocol spec as client (from relay to master)

	 Obtain a copy of the blockchain
		GET /blockchain
			 Response code 200 : a json list with
					[
					 {
						ID: block id,
						DATA: block data,
						Hash: hash of the block   
					 },
					 ...       
					]
	 submit a block
		POST /blockchain with this JSON
			Rquest data, a json with
			 {
				HASH: hash,
				DATA: block data            
			 }
			response
			 if success 200 with this JSON
				{
					 ID: block ID
				}

"""
