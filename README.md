# How to compile

For this project, we'll use Python 3.

You'll have to install the pycrypto library (version 2.6.1) - you can download it on https://www.dlitz.net/software/pycrypto/

Make sure that you have the package request installed in order to handle network.
You can find inside the file install of Network folder, required command line for package request installation.

For the database, we use SQLite as we don't have huge needs. However, all the requests are compatible with MYSQL if we want to reach more persons.

# How to setup the network

Nothing special to do. Just launch the program and it will create a local network. All the data received and sent by the server are in JSON. This format is a bit verbose but still easily readable.

For the communication between the client and the server, we use the http protocol.

The relay nodes handle two types of requests :
  - GET : get the list of pending transactions or get the last block of the blockchain.
  - POST : submit a new transaction to be processed by the network or submit the new mined blocks to the user who requested an update of the chain.

The master node also handle GET and POST requests :
  - GET : get the last block of the blockchain.
  - POST : submit the new mined blocked to the relay nodes.

# How to use the wallet

The user has to give a login and a password to use the wallet. If the user doesn't exist, a new wallet for this user is automatically created and the wallet download the blockchain. Otherwise, the user is connected to his wallet and the blockchain is updated.

If the wallet countains some coins, the user is able to make some transactions. The network doesn't allow transactions of less than 1 coin or negative transactions (ie Alice can not send -3 coins or 0.5 to Bob). Obviously, he can not sent more coins than he has in his wallet. It is not possible to make a transaction with an already used address.

To make a transaction, the user must type the command 'transaction'. Then he has to specify the address of the receiver and the amount he wants to send.
If the transaction fullfill the conditions of the above paragraph, a new adress (a public key and a private key) is generated for the wallet. 

After those steps, the transaction is submitted to a relay node and the new adress of the wallet is stored in the local database.
