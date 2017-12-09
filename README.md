# How to compile

For this project, we'll use Python 3.
To compile the project, you'll have to install the pycrypto library (version 2.6.1) - you can download it on https://www.dlitz.net/software/pycrypto/


# How to setup the network

# How to use the wallet

The user has to give a login and a password to use the wallet. If the user doesn't exist, a new wallet for this user is automatically created.
Otherwise, the user is connected to his wallet.

If the wallet countains some coins, the user is able to make some transactions. The network doesn't allow transactions of 0 coin or negative transactions (ie Alice sent -3 coins to Bob is not possible)
