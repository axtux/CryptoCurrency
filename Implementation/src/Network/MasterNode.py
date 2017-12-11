#!/usr/bin/env python3
import json

from http.server import BaseHTTPRequestHandler, HTTPServer

import sys
sys.path.insert(0,'..')
from block import Block


MY_IP='127.0.20.1'
IP_RELAY = [
	"127.0.1.1",
	"127.0.2.1",
	"127.0.3.1",
]

"""
    MAN
        for wallet
            to implement:  (see pre/post cond.)
                getBlockChain()
                submitBlock(block)
"""

### TO IMPLEMENT
"""
    input: none
    ouput: array with all block objetc
"""
def getBlockChain():
    #TODO get blocks
    blocks=[]
    return blocks

"""
    input: The block ojcet to add
    ouput: True if succes, execption else
"""
def submitBlock(block):
    #TODO add to block chain
    return True


# HTTPRequestHandler class
class testHTTPServer_RequestHandler(BaseHTTPRequestHandler):

    def handleGet(self):
        return json.dumps([ v.toJson() for v in getBlockChain()])

    def handlePost(self,data):
        return submitBlock(Block.fromJson(data))

    # GET
    def do_GET(self):
        # Send response status code
        self.send_response(200)

        # Send headers
        self.send_header('Content-type','text/html')
        self.end_headers()

        # Send message back to client
        message = str(self.handleGet())
        # Write content as utf-8 data
        self.wfile.write(bytes(message, "utf8"))
        return

  # POST
    def do_POST(self):
        data = (self.rfile.read(int(self.headers['Content-Length'])).decode("utf-8") )

        # Send response status code
        self.send_response(200)

        # Send headers
        self.send_header('Content-type','text/html')
        self.end_headers()

        # Send message back to client
        message = str(self.handlePost(data))
        # Write content as utf-8 data
        self.wfile.write(bytes(message, "utf8"))
        return

def run():
    print('starting server...')

    # Server settings
    # Choose port 8080, for port 80, which is normally used for a http server, you need root access
    server_address = (MY_IP, 8081)
    httpd = HTTPServer(server_address, testHTTPServer_RequestHandler)
    print('running server...')
    httpd.serve_forever()

if __name__ == '__main__':
    run()


"""

	protocol spec
	from relay to master (master is the server)
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
