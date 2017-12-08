#!/usr/bin/env python 
import requests
import json
from random import randint
from ..transaction import Transaction

MAX_ITER = 5
IP_RELAY = [
	"http://127.0.1.1:8081",
	"http://127.0.1.1:8081",
	"http://127.0.1.1:8081",
]
"""
	MAN
		to submit a transactio to the relay node
			call postTransaction(trans) 
				where trans is a Transaction object
				return the ID of the ransaction

		to get a transactio to the relay node
			call getTransaction(ID) 
				where ID is the id of the transaction object
				return an array with the id and a Transactionobject

		see doTest method for an exemple


"""
#  Get transaction

def getNumber():
	return (randint(0, len(IP_RELAY)))
	

def makeGet(server, id):
	data = False
	print("ygg")
	print(server)
	r = requests.get(str(server)+"/transaction/"+str(id))
	
	if r.status_code==200:
		return r.text
	else:
		raise Exception()

def getTransaction(id):
	i=0
	start= getNumber();
	while (i<MAX_ITER):
		try:
			print(start)
			print(IP_RELAY[start])
			res = makeGet(IP_RELAY[start], id)
			js =  json.loads(res)
			js[1] = Transaction().fromJson(json.dumps(js[1]))
			return js
		except:
			i +=1
			start	= (start + 1) % len(IP_RELAY)
		
		
#  post transaction
	

def makePost(server, data):
	data = False
	r = requests.post(str(server)+"/transaction/",data=data)
	
	if r.status_code==200:
		return r.text
	else:
		raise Exception()

def postTransaction(transaction):
	i=0
	start= getNumber();
	while (i<MAX_ITER):
		try:
			return makePost(IP_RELAY[start], transaction.toJson())
		except:
			i +=1
			start	= (start + 1) % len(IP_RELAY)	
		
		
		
def doTest():	
	trans = Transaction("moi",42,"toi")
	
	id =  postTransaction(trans)
	trans2 = getTransaction(id)
	
	if id==trans2[0]:
		print("trans id ok")
	else:
		print("trans id ko")
		
	if json.dumps(trans)==json.dumps(trans2[1]):
		print("trans ok")
	else:
		print("trans ko")
		
		
		
"""
	protocol spec client
		GET /transaction/ID
				Response code 200 : a json list with
							{
								"ID": block id,								
								"sender:sender,
								"amount":amount,
								"receiver":amout	
							}
		POST /transaction
					Reuest: a json {	
						"sender":sender,
						"amount":amount,
						"receiver":amout
					}

					Response code 200 : 
						response json {
							"ID": block id,	
						}

"""
