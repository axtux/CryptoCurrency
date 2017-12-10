import block

class Master(object):
    """docstring for Master node.
        His role is to update and stock the block chain
        He only comunicate with the relay nodes


        """
    def __init__(self):
        self.queue = [] #vérifier que dépasse pas une certaine taille
        self.bc = Blockchain()#changer en blockchain initialisation
        self.addr = [] #changer en hradcodant les IP des relay nodes

    def addBlock(self,block) :
        """
            This function add the block given by the relay node to the queue ( max 100)
        """
        if (len(self.queue)<= 100):
            self.queue.append(block)
        return None

    def update(self) :
        """
        This function is used to update the blockChain.
        It would get the first block in the list given by relay nodes that correspond with the current state.
        if this block exists , we update the current state of the blockchain.
        otherwise, we don't do nothing
        """
        for b in self.queue :
            if (correspond(b)) :
                self.bc.add_block(b)
                break
        self.queue = [] #we discard the remaining blocks
        return None

    def correspond(self, block):
        """
            This function is used to check if the hash of a block correspond with the current block of the blockchain
        """
            pass
