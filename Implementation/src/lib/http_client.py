import requests
from random import randint

# local imports
from lib.network import Network
from lib.transaction import Transaction
from lib.block import Block


class MasterClient(object):
    
    def __init__(self):
        s = Network.get_master()
        self.url = 'http://'+s[0]+':'+s[1]+'/'
    
    def get_block(self, previous_hash):
        """send GET request to self.url/blocks/previous_hash
        """
        r = requests.get(self.url+'blocks/'+previous_hash)
        if not r.status.code == 200:
            return None
        return Block.fromJson(r.text())

    def submit_block(self, block):
        """send POST request with JSON encoded block to self.url/blocks/
        """
        data = block.toJson()
        r = requests.post(base_url+'blocks/', data=data)
        if r.status_code == 200:
            return True
        return False


class RelayClient(MasterClient):
    
    def __init__(self, relay=None):
        """initialite an http client to request the relay server
        if relay is None, random relay is chosen from Network
        """
        servers = Network.get_relays()
        if relay == None
            relay = servers[randint(0, len(servers)-1)]
        self.url = 'http://'+relay[0]+':'+relay[1]+'/'

    def get_transactions(self):
        """send GET request to relay/transactions/ and parse it
        """
        r = requests.get(self.url+'transactions/')
        if not r.status.code == 200:
            return None
        try:
            json_ts = r.json()
        except ValueError e:
            return None
        ts = []
        for json in json_ts:
            t = Transaction.fromJson(json)
            if t != None:
                ts.append(t)
        return ts

    def submit_transaction(self, transaction):
        """send POST request with JSON encoded transaction to relay/transactions/
        """
        data = transaction.toJson()
        r = requests.post(base_url+'transactions/', data=data)
        if r.status_code == 200:
            return True
        return False
