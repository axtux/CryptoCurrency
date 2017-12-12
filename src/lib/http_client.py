import requests
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from random import randint

# local imports
from lib.network import Network
from lib.transaction import Transaction
from lib.block import Block
from lib.log import warning

def get_request(url):
    r = None
    try:
        r = requests.get(url)
    except ConnectionError:
        warning('http connection error')
    except Timeout:
        warning('http timeout')
    except TooManyRedirects:
        warning('http too many redirects')
    return r

def post_request(url, data):
    r = None
    try:
        r = requests.post(url, data=data)
    except ConnectionError:
        warning('http connection error')
    except Timeout:
        warning('http timeout')
    except TooManyRedirects:
        warning('http too many redirects')
    return r

class MasterClient(object):

    def __init__(self):
        s = Network.get_master()
        self.url = 'http://'+s[0]+':'+str(s[1])+'/'

    def get_block(self, previous_hash):
        """send GET request to self.url/blocks/previous_hash
        """
        r = get_request(self.url+'blocks/'+previous_hash)
        if r is None:
            return None
        if not r.status_code == 200:
            return None
        return Block.fromJson(r.text)

    def submit_block(self, block):
        """send POST request with JSON encoded block to self.url/blocks/
        """
        data = block.toJson()
        r = post_request(self.url+'blocks/', data)
        if r is None:
            return False
        if r.status_code == 200:
            return True
        return False


class RelayClient(MasterClient):

    def __init__(self, relay=None):
        """initialize an http client to request the relay server
        if relay is None, random relay is chosen from Network
        """
        servers = Network.get_relays()
        if relay is None:
            relay = servers[randint(0, len(servers)-1)]
        self.url = 'http://'+relay[0]+':'+str(relay[1])+'/'

    def get_transactions(self):
        """send GET request to relay/transactions/ and parse it
        """
        r = get_request(self.url+'transactions/')
        if r is None:
            return None
        if not r.status_code == 200:
            return None
        try:
            json_ts = r.json()
        except ValueError:
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
        r = post_request(self.url+'transactions/', data)
        if r is None:
            return False
        if r.status_code == 200:
            return True
        return False
