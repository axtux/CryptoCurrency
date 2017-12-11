# How to compile

For this project, we'll use Python 3.
To compile the project, you'll have to install the pycrypto library (version 2.6.1) - you can download it on https://www.dlitz.net/software/pycrypto/

Before compiling the project, make sure that you have the  package  request installed in order to handle network.
You can find inside the file install of Network folder, required command line for package  request installation.

# How to setup the network

Nothing special to do. Just launch the program and it will create a local network. All the data received and sent by the server are in JSON.

# How to use the wallet

The user has to give a login and a password to use the wallet. If the user doesn't exist, a new wallet for this user is automatically created.
Otherwise, the user is connected to his wallet.

If the wallet countains some coins, the user is able to make some transactions. The network doesn't allow transactions of 0 coin or negative transactions (ie Alice sent -3 coins to Bob is not possible).

Before each transaction, a new adress (a public key and a private key) is generated for the wallet. Once the transaction is done, the new adress is stored in the local database.
