

class Network(object):
    
    def get_master():
        return ('127.42.42.1', '8080')
    
    def get_relays():
        return [
            ('127.42.1.1', '8080'),
            ('127.42.1.2', '8080'),
            ('127.42.1.3', '8080')
        ]

"""
All data are returned JSON encoded

Response code :
    200 => success
    204 => no content (empty response)
    4xx => client error
    5xx => server error

    Master and relay requests:
GET /blocks/previous_hash
    get the block after previous_hash
POST /blocks/
    submit the new mined block

=== Relay server ===
GET /transactions/
    get list of pending transactions
POST /transactions/
    submit a new transaction to be processed by the network
"""

if __name__ == '__main__':
    print(Network.get_relays())
