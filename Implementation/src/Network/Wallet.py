#!/usr/bin/env python 
import requests
from random import randint

MAX_ITER = 5
IP_RELAY = [
	"http://127.0.1.1:8081",
	"http://127.0.1.1:8081",
	"http://127.0.1.1:8081",
]
"""
	protocol spec client
		GET /transaction/ID
				Response code 200 : a json list with
							{
								ID: block id,
								DATA: data,
								Hash: hash of the block		
							}
		POST /transaction
					Response code 200 : a json list with
							{
								..
							},


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
			return makeGet(IP_RELAY[start], id)
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

def postTransaction(data):
	i=0
	start= getNumber();
	while (i<MAX_ITER):
		try:
			return makePost(IP_RELAY[start], data)
		except:
			i +=1
			start	= (start + 1) % len(IP_RELAY)	
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
