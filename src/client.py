from lib.walletConnection import Connection
from lib.utils import sha_256
from lib.address import Address
import os

def showDetails(wallet):
    print(wallet.user_ID)
    #wallet.checkUpdate()
    print(str(wallet.addr) + " => " + str(wallet.count))
    print("\n\n\nIt's possible that this value was not up-to-date. Please, want some minutes to validate the last transaction")

def makeTransaction(wallet):
    clear()
    addr  = input("Please, enter the address to send the money\n")
    money = input("Please, enter the amount of money do you want to send to "+addr+"\n")
    receivers = [ (addr,int(money)) ]
    while True:
        again = input("Do you want to make an another transfer in your transaction ? (y or n)")
        while again != 'y' and again != 'n':
            again = input("Do you want to make an another transfer in your transaction ? (y or n)")
        if again == 'y':
            addr  = input("Please, enter the address to send the money\n")
            money = input("Please, enter the amount of money do you want to send to "+addr+"\n")
            receivers.append( (addr,money) )
        elif again == 'n':
            print("\n\n\n")
            break
    password = input("Please, enter your password to valid the Transaction\n")
    isValid = wallet.createTransaction(password, receivers)
    if not isValid:
        print("Sorry, but your Transaction is not valid")

def manuel():
    print("This is a list of possible command : \n")
    print("show   : Show your Wallet information with the money in your address")
    print("trans  : Create a new transaction")
    print("back   : Go back to an ald address if your last transaction was not validate")

def backAddress(wallet):
    """Return to the previous address
    """
    wallet.backAddress()

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

if __name__ == '__main__':
    conn = Connection()
    clear()
    print("Hello")
    isNew = input("Are you a new user ? (y or n or help)\n")
    while isNew != 'y' and isNew != 'n':
        if isNew == 'help':
            clear()
            print("If it's the first time you use this application, type 'y' to create your Wallet")
            print("If you already have a Wallet, type 'n' to connecte to your Wallet")
        isNew = input("Are you a new user ? (y or n or help)\n")
    clear()

    user_ID = input("Please, enter your user ID\n")
    clear()
    password = input("Please, enter your password\n")
    clear()
    isNew = (isNew == 'y')    #True if 'y', False if 'n'
    wallet = conn.allowConnection(user_ID, password, isNew)
    while wallet is None:
        print("You make a mistake, please retry")
        if isNew:
            print("Maybe this user ID already exist")
        else:
            print("Maybe your user ID or password are incorrect")
        print("\n\n")
        user_ID = input("Please, enter your user ID again\n")
        clear()
        password = input("Please, enter your password again\n")
        clear()
        wallet = conn.allowConnection(user_ID, password, isNew)

    command = 'show'
    while command != 'close':
        if command == 'show':
            showDetails(wallet)
        if command == 'trans':
            makeTransaction(wallet)
        if command == 'back':
            backAddress(wallet)
            showDetails(wallet)
        if command == 'man':
            manuel()
        print("\n\n\n")
        manuel()
        print()
        command = input("What do you what to do ? (type 'man' for the list of action)")

    print("Good Bye !")
