#!/usr/bin/env python 
from http.server import BaseHTTPRequestHandler, HTTPServer
import requests

MY_IP= '127.0.1.1'
MASTER_URL = 'http://127.0.20.1:8081'

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
		return getBlockchain()
	def postTransactionResponse(self):
		return submitBlockchain({})
	
	def getWorkResponse(self):
		return submitBlockchain({})
		
	def submitWorkResponse(self):
		pass
 
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

			self.send_header('Content-type','text/html')
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
			if self.path == "/transaction/":
				resp = self.postTransactionResponse()
			elif self.path == "/submitBlock" :
				resp = self.submitWorkResponse()        
			else:        
				self.send_error(404, str(self.path)+" not found")
				return

			self.send_header('Content-type','text/html')
			self.end_headers()
	 
			self.wfile.write(bytes(str(resp), "utf8"))
			return
		except Exception as e:
			self.send_error(500, str(e))

 
def run():
	print('starting server...')
 
	# Server settings
	# Choose port 8080, for port 80, which is normally used for a http server, you need root access
	server_address = (MY_IP, 8081)
	httpd = HTTPServer(server_address, testHTTPServer_RequestHandler)
	print('running server...')
	httpd.serve_forever()
 
 
run()




