from http.server import BaseHTTPRequestHandler, HTTPServer
from random import randint
import json

# local imports
from lib.network import Network
from lib.transaction import Transaction
from lib.block import Block
from lib.blockchain import Blockchain
from lib.http_client import MasterClient, RelayClient
from lib.log import debug

class EasyHandler(BaseHTTPRequestHandler):
    error_message_format = ''

    def no_response(self, code):
        self.send_response(code)
        self.end_headers()

    def json_response(self, code, json=''):
        self.send_response(code)
        self.send_header('Content-type', 'application/json; charset=UTF-8')
        self.end_headers()
        self.wfile.write(bytes(json, 'UTF-8'))

    def post_body(self):
        if 'Content-Length' in self.headers:
            l = self.headers['Content-Length']
            return self.rfile.read(int(l)).decode('UTF-8')
        else:
            return self.rfile.read().decode('UTF-8')

    def get_block(self, previous_hash):
        block = self.server.blockchain.get_next_block(previous_hash)
        if block is None:
            self.no_response(204) # No Content
        else:
            self.json_response(200, block.toJson())

    def post_block(self, json):
        b = Block.fromJson(json)
        if b is None:
            debug('JSON error')
            self.no_response(400) # Bad Request
        elif not self.server.blockchain.add_block(b):
            debug('invalid block')
            self.no_response(400) # Bad Request
        else:
            self.no_response(200) # OK
            return b


class MasterServer(HTTPServer):
    def __init__(self, server_address, blockchain):
        super().__init__(server_address, MasterHandler)
        self.blockchain = blockchain
        rs = Network.get_relays()
        self.relays = [r[0] for r in rs]
        print('Server started on '+server_address[0]+':'+str(server_address[1]))

class MasterHandler(EasyHandler):
    error_message_format = ''

    def allowed_client(self):
        """check that the client is relay node
        """
        ip = self.client_address[0]
        return ip in self.server.relays

    def do_GET(self):
        if not self.allowed_client():
            self.no_response(401) # Unauthorized
        elif self.path[:8] == '/blocks/':
            previous_hash = self.path[8:]
            self.get_block(previous_hash)
        else:
            self.no_response(404) # Not Found

    def do_POST(self):
        json = self.post_body()
        if not self.allowed_client():
            self.no_response(401) # Unauthorized
        elif self.path == '/blocks/':
            self.post_block(json)
        else:
            self.no_response(404) # Not Found

class RelayServer(HTTPServer):
    def __init__(self, server_address, blockchain):
        super().__init__(server_address, RelayHandler)
        self.blockchain = blockchain
        self.master = MasterClient()
        self.transactions = []
        # HTTP client relays, used to broadcast transactions
        self.relays = []
        for r in Network.get_relays():
            if r != server_address:
                self.relays.append(RelayClient(r))
        print('Server started on '+server_address[0]+':'+str(server_address[1]))

class RelayHandler(EasyHandler):
    error_message_format = ''

    def post_block(self, json):
        # TODO submit to master before response
        b = EasyHandler.post_block(self, json)
        if not b is None:
            # if block is ok, submit to master
            self.server.master.submit_block(b)
            self.check_transactions()

    def get_transactions(self):
        json_ts = [t.toJson() for t in self.server.transactions]
        self.json_response(200, json.dumps(json_ts))

    def post_transaction(self, json):
        t = Transaction.fromJson(json)
        if t is None:
            debug('JSON error')
            self.no_response(400) # Bad Request
        elif not t.is_valid(self.server.blockchain):
            debug('invalid blockchain transaction')
            self.no_response(400) # Bad Request
        else:
            self.server.transactions.append(t)
            self.no_response(200) # OK
            self.broadcast_transaction(t)

    def check_transactions(self):
        # remove invalid transactions
        self.server.transactions = list(filter(
            lambda t: t.is_valid(self.server.blockchain),
            self.server.transactions
        ))

    def broadcast_transaction(self, t):
        for r in self.server.relays:
            r.post_transaction(t)

    def do_GET(self):
        if self.path[:8] == '/blocks/':
            previous_hash = self.path[8:]
            self.get_block(previous_hash)
        elif self.path == '/transactions/':
            self.get_transactions()
        else:
            self.no_response(404) # Not Found

    def do_POST(self):
        json = self.post_body()
        if self.path == '/blocks/':
            self.post_block(json)
        elif self.path == '/transactions/':
            self.post_transaction(json)
        else:
            self.no_response(404) # Not Found
