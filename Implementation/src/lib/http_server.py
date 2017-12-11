from http.server import BaseHTTPRequestHandler, HTTPServer
from random import randint

# local imports
from lib.network import Network
from lib.transaction import Transaction
from lib.block import Block
from lib.blockchain import Blockchain


class EasyHandler(BaseHTTPRequestHandler):
    error_message_format = ''

    def no_response(self, code):
        self.send_response(code)
        self.end_headers()
    
    def json_response(self, code, json=''):
        self.send_response(code)
        self.send_header('Content-type', 'application/json; charset=UTF-8')
        self.end_headers()
        self.wfile.write(bytes(content, 'UTF-8'))
    
    def get_block(self, previous_hash):
        block = self.server.blockchain.get_next_block(previous_hash)
        if block == None:
            self.no_response(204) # No Content
        else:
            self.json_response(200, block.toJson())
    
    def post_block(self, json):
        b = Block.fromJson(json)
        if b == None:
            self.no_response(400) # Bad Request
        elif not self.server.blockchain.add_block(b):
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

class MasterHandler(BaseHTTPRequestHandler):
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
        json = self.rfile.read().decode('UTF-8')
        if not self.allowed_client():
            self.no_response(401) # Unauthorized
        elif self.path == '/blocks/':
            self.post_block(json)
        else:
            self.no_response(404) # Not Found

class RelayServer(HTTPServer):
    def __init__(self, server_address, blockchain, master):
        super().__init__(server_address, RelayHandler)
        self.blockchain = blockchain
        self.master = master
        self.transactions = []
        # HTTP client relays, used to broadcas transactions
        self.relays = []
        for r in Network.get_relays():
            if r != server_address:
                self.relays.append(RelayClient(r))
        print('Server started on '+server_address[0]+':'+str(server_address[1]))

class RelayHandler(BaseHTTPRequestHandler):
    error_message_format = ''
    
    def post_block(self, json):
        # TODO submit to master before response
        b = EasyHandler.post_block(self, json)
        if not b == None:
            # if block is ok, submit to master
            self.server.master.submit_block(block)

    def get_transactions(self):
        json_ts = [t.toJson() for t in self.server.transactions]
        self.json_response(200, json.dumps(json_ts)
    
    def post_transaction(self, json):
        t = Transaction.fromJson(json)
        if t == None:
            self.no_response(400) # Bad Request
        elif not t.is_valid(self.server.blockchain):
            self.no_response(400) # Bad Request
        else:
            self.server.transactions.append(t)
            self.no_response(200) # OK
            self.broadcast_transaction(t)
    
    def broadcast_transaction(t):
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
        json = self.rfile.read().decode('UTF-8')
        if self.path == '/blocks/':
            self.post_block(json)
        elif self.path == '/transactions/':
            self.post_transaction(json)
        else:
            self.no_response(404) # Not Found
