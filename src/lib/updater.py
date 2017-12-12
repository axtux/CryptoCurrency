# local imports
from lib.blockchain import Blockchain
from lib.utils import sha_256
from lib.address import Address
from lib.http_client import RelayClient
from lib.log import debug

class Updater(object):
    def __init__(self, blockchain, relay=None):
        self.blockchain = blockchain
        if relay == None:
            self.relay = RelayClient()
        else:
            self.relay = relay

    def update(self):
        """Update the blockchain from relay
           Stop when blockchain is updated (next block is None)
           Return True if updated, False if not
        """
        debug('updating blockchain')
        updated = False
        new_block = self.relay.get_block(self.blockchain.get_last_hash())
        while not new_block is None:
            debug('got block '+new_block.get_hash())
            updated = True
            self.blockchain.add_block(new_block)
            new_block = self.relay.get_block(self.blockchain.get_last_hash())
        return updated
