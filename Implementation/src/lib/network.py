

class Network(object):
    
    def get_master():
        return ('127.42.42.1', '8080')
    
    def get_relays():
        return [
            ('127.42.1.1', '8080'),
            ('127.42.1.2', '8080'),
            ('127.42.1.3', '8080')
        ]

if __name__ == '__main__':
    print(Network.get_relays())
