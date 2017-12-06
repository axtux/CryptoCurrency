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

#  Get transaction

def getNumber():
	return (randint(0, len(IP_RELAY)))
	

def makeGet(server, id):
	data = False
	r = requests.get(server+"/getWork/")
	
	if r.status_code==200:
		return r.text
	else:
		raise Exception()

def getWork(id):
	i=0
	start= getNumber();
	while (i<MAX_ITER):
		try:
			return makeGet(IP_RELAY[start], id)
		except:
			i +=1
			start	= (start + 1) % len(IP_RELAY)
			print(e)
		
		
#  post transaction
	

def makeSubmit(server, data):
	data = False
	r = requests.post(server+"/submitTransaction/",data=data)
	
	if r.status_code==200:
		return r.text
	else:
		raise Exception()

def submitTrasaction(data):
	i=0
	start= getNumber();
	while (i<MAX_ITER):
		try:
			return makeSubmit(IP_RELAY[start], data)
		except:
			i +=1
			start	= (start + 1) % len(IP_RELAY)	
			print(e)
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
