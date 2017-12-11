

class Network(object):
    
    def get_master():
        return ('127.42.42.1', 8080)
    
    def get_relays():
        return [
            ('127.0.0.1', 8080),
            ('127.42.1.1', 8080),
            ('127.42.1.2', 8080),
            ('127.42.1.3', 8080)
        ]

"""
All data must be sent and is returned JSON encoded

=== Master and relays ===
GET /blocks/PREVIOUS_HASH
    get the block after previous_hash
    Possible response code:
        204: no block next
        200: block returned
POST /blocks/
    submit the new mined block
    Possible response code:
        400: bad JSON or bad block (can be too late)
        200: block saved

=== Relays only ===
GET /transactions/
    get list of pending transactions
    Possible response code:
        200: transactions returned
POST /transactions/
    submit a new transaction to be processed by the network
    Possible response code:
        400: bad JSON or bad transaction (can be too late)
        200: block saved
"""

if __name__ == '__main__':
    print(Network.get_master())
    print(Network.get_relays())
