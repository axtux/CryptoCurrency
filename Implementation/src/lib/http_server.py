from http.server import BaseHTTPRequestHandler, HTTPServer
from random import randint

# local imports
from lib.network import Network
from lib.transaction import Transaction
from lib.block import Block
from lib.blockchain import Blockchain

class MasterServer(HTTPServer):
    def __init__(self, server_address, blockchain):
        super().__init__(server_address, MasterHandler)
        self.blockchain = blockchain
        rs = Network.get_relays()
        self.relays = [r[0] for r in rs]
        print('Server listening on '+server_address[0]+':'+str(server_address[1]))
        self.serve_forever()
    
    def start(ip, port, handler):
        """Start an HTTP server on ip:port with handler
        """
        print('Starting HTTP server...')
        httpd = MasterServer((ip, port), handler)
        httpd.serve_forever()


class MasterHandler(BaseHTTPRequestHandler):
    error_message_format = ''

    def check_client(self):
        """check that the client is relay node
        """
        ip = self.client_address[0]
        if not ip in self.server.relays:
            #self.send_error(401)
            pass
    
    def json_response(self, code, content=''):
        self.send_response(code)
        self.send_header('Content-type', 'application/json; charset=UTF-8')
        self.end_headers()
        self.wfile.write(bytes(content, 'utf8'))
    
    def do_GET(self):
        self.check_client()
        if self.path[:8] == '/blocks/':
            previous_hash = self.path[8:]
            # TODO send block
            self.json_response(200, 'previous_hash='+previous_hash)
        else:
            self.json_response(404)
            
    
    def do_POST(self):
        self.check_client()
        if self.path == '/blocks/':
            json = self.rfile.read()
            # TODO decode and send to blockchain
            print('POST '+json)
        else:
            self.json_response(404)
