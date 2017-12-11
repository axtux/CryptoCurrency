from lib.walletConnection import Connection

if __name__ == '__main__':
    conn = Connection()
    print("Hello")
    isNew = input("Are you a new user ? (y or n or help)\n")
    while isNew != 'y' or isNew != 'y':
        if isNew == 'help':
            print("If it's the first time you use this application, type 'y' to create your Wallet")
            print("If you already have a Wallet, type 'n' to connecte to your Wallet")
        isNew = input("Are you a new user ? (y or n or help)\n")

    user_ID = input("Please, enter your user ID\n")
    password = input("Please, enter your password\n")
    isNew = isNew == 'y'    #True if 'y', False if 'n'
    wallet = conn.allowConnection(user_ID, password, isNew)
    wallet = None
    while wallet != None:
        print("You make a mistake, please retry")
        user_ID = input("Please, enter your user ID again\n")
        password = input("Please, enter your password again\n")
        isNew = (isNew == 'y')    #True if 'y', False if 'n'
        wallet = conn.allowConnection(uer_ID, password, isNew)

    showDetails(wallet)



def showDetails(wallet):
    print(wallet.user_ID)
    wallet.checkUpdate()
    print(wallet.addr + " => " + wallet.count)
