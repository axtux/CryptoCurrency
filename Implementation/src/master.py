from lib.blockchain import Blockchain
from lib.network import Network
from lib.http_server import MasterServer

if __name__ == '__main__':
    b = Blockchain('master')
    master = Network.get_master()
    server = MasterServer(master, b)
    server.serve_forever()
