import sys

# local imports
from lib.blockchain import Blockchain
from lib.network import Network
from lib.http_server import RelayServer

if __name__ == '__main__':
    argc = len(sys.argv)
    if not argc == 2:
        exit('usage: python3 '+sys.argv[0]+' RELAY_NUMBER')
    relays = Network.get_relays()
    n = len(relays)
    i = int(sys.argv[1]) % n
    print('Starting relay '+str(i))
    b = Blockchain('relay'+str(i))
    master = Network.get_master()
    server = RelayServer(relays[i], b)
    server.serve_forever()
    # TODO update blockchain in background or receive pushes from server
