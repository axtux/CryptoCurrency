import requests

from random import randint


import sys
sys.path.insert(0,'..')
from block import Block

MAX_ITER = 5
IP_RELAY = [
	"http://127.0.1.1:8081",
	"http://127.0.1.1:8081",
	"http://127.0.1.1:8081",
]

"""
	MAN
		to get work 
			call getWork() 
				it return a block object without hash
		to submit work
			call submitBlock(block)
				input take a block object 
				it return True or Exeption

		see doTest for exemples
"""
#  Get transaction

def getNumber():
	return (randint(0, len(IP_RELAY)-1))
	

def makeGet(server):
	data = False
	r = requests.get(server+"/getWork/")
	print(r.text)
	
	if r.status_code==200:
		return r.text
	else:
		print("eoi")
		raise Exception()

def getWork():
	i=0
	start= getNumber();
	while (i<MAX_ITER):
		try:
			return Block.fromJson(makeGet(IP_RELAY[start]))
		except Exception as e:
			i +=1
			start	= (start + 1) % len(IP_RELAY)
			raise e
		
		
#  post transaction
	

def makeSubmit(server, data):
	r = requests.post(server+"/submitBlock/",data=data)
	
	if r.status_code==200:
		return True
	else:
		print()
		raise Exception(r.text)

def submitBlock(block):
	i=0
	start= getNumber();
	while (i<MAX_ITER):
		try:
			return makeSubmit(IP_RELAY[start], block.toJson())
		except Exception as e:
			i +=1
			start	= (start + 1) % len(IP_RELAY)
			raise (e)
		
		
		
		
def doTest():
	block= getWork()
	try:		
		if(submitBlock(block)):
			print("ok")
	except Exception as e:
		print("ko")
		
		
		
		
		
		
"""
	protocol spec client
		GET /getWork
				Response code 200 : a json list with
							{
								ID: block id,
								DATA: data,	
							}
		POST /submitTransaction
					Response code 200 : a json list with
							{
								ID: block id,
								DATA: data,	
								HASH: proof of work
							}
		
	"""	
		
		
		
		
		
		
		
		
		
		
		
		
		
