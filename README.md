# How to use

# Prerequisites
You need :
- Python 3
- the requests and sqlite3 package
- the PyCrypto library available at https://www.dlitz.net/software/pycrypto/

# Master
To launch master server, run the following command :
```bash
$ python3 master.py
```

# Relay
To launch a relay server, run the following command :
```bash
$ python3 relay.py RELAY_NUMBER
```

# Miner
To launch miner, run the following command :
```bash
$ python3 miner.py MINER_ADDRESS
```

# Client
To launch client, run the following command :
```bash
$ python3 client.py COMMAND
```

# Commands
The following commands are available :
- `list` to list addresses with amount available
- `new` to create new address
- `transfer FROM_ADDRESS TO_ADDRESS AMOUNT` to transfer money

# Network
Network IP addresses can be setup within `lib/network.py`. Requests are made in JSON format over HTTP. Here's the API description :

## Master and relay nodes
```
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
```

## Relay nodes only
```
GET /transactions/
    get list of pending transactions
    Possible response code:
        200: transactions returned
POST /transactions/
    submit a new transaction to be processed by the network
    Possible response code:
        400: bad JSON or bad transaction (can be too late)
        200: block saved
```
