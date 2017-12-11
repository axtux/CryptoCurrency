import logging

# local imports
from lib.blockchain import Blockchain
from lib.utils import sha_256
from lib.address import Address
from lib.http_client import RelayClient

class Updater(object):
    def __init__(self, blockchain):
        self.blockchain = blockchain
        self.relay = RelayClient()
        self.log = logging.getLogger(__name__)
    
    def update(self):
        """Update the blockchain from relay
           Stop when blockchain is updated (next block is None)
           Return True if updated, False if not
        """
        log.debug('updating blockchain')
        updated = False
        new_block = self.relay.get_block(self.blockchain.get_last_hash())
        while new_block != None:
            log.debug('found block '+block.get_hash())
            updated = True
            self.blockChain.add_block(new_block)
            new_block = self.relay.get_block(self.blockchain.get_last_hash())
        return updated
