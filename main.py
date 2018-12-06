import getpass, os,sys
from Crypt import encrypt_file
from Crypt import decrypt_file
import shutil
from Crypto.Hash import SHA256

def welcome_screen():
    print("Data Locker\n1.Login\n2.Create Account\n3.Exit")
    ch = input()
    if ch==1:
        login()
    elif ch==2:
        create_account()
    else:
        print("Closing program")

def check_pass(string, hashedstring):
    hashboy = SHA256.new()
    hashboy.update(string.encode('utf-8'))
    if hashboy.digest() == hashedstring:
        return True
    else:
        #print('\n%s\n %s\n %s',string,hashedstring,hashboy.digest())
        return False

def add_account(user_id, password):
    with open('Userlist.txt','a') as userlist:
        hashpass = SHA256.new()
        hashpass.update(password.encode('utf-8'))
        userlist.write(user_id + ' ' + hashpass.digest() + '\n')

    directory = os.getcwd()+'/Data/'+user_id
    if not os.path.exists(directory):
        os.makedirs(directory)

def list_data(user_id, password):
    encfilelist = os.listdir(os.getcwd()+'/Data/' + user_id)
    i=0
    for encfile in encfilelist:
        i=i+1
        print(str(i)+' '+encfile+'\n')

    print('1. Encrypt New File \n2. Decrypt File\n3. Return\n')
    ch = input('Enter choice: ')
    #print(ch)

    if(ch == 3):
        return

    if(ch == 2):
        dead = input('\nEnter index of file to decrypt: ')
        filepath = os.getcwd() + '/Data/' + user_id +'/'+ encfilelist[dead-1]
        hashpass = SHA256.new()
        hashpass.update(password.encode('utf-8'))
        origfile = decrypt_file(hashpass.digest(), filepath)
        os.remove(filepath)
        location = raw_input('\nWhere do you want the decrypted file to be? ')
        shutil.move(origfile,location)
        list_data(user_id, password)

    if(ch == 1):
        filepath = raw_input('\nEnter File Path: ')
        newfilepath = os.getcwd()+ '/Data/' + user_id + '/' + filepath.split('/')[-1]
        shutil.move(filepath, newfilepath )#file moved
        hashpass = SHA256.new()
        hashpass.update(password.encode('utf-8'))
        encrypt_file(hashpass.digest(), newfilepath)
        if os.path.exists(newfilepath):
            os.remove(newfilepath)
        list_data(user_id, password)


def check_exists(user_id, password):
    with open('Userlist.txt','r') as userlist:
        while True:
            line = userlist.readline()
            curr = line.split()
            if(line == ''):
                return False #end of file reached
            if curr[0] == user_id:
                #print("\nFuck")############################################
                return check_pass(password, curr[1])#check if hash of first arg is the second arg

def check_unique(user_id):
    with open('Userlist.txt','r') as userlist:
        while True:
            line = userlist.readline()
            curr = line.split()
            if line == '':
                return  True
            if curr[0] == user_id:
                return False


def getinfo():
    user_id = raw_input('\nEnter User ID (no blank space): ')
    if ' ' in user_id:
        print('I said NO SPACE !!!')
        getinfo()
    #user_id = '\'' +user_id+ '\''

    password = getpass.getpass('\nEnter password: ')
    if ' ' in password:
        print('I said NO SPACE !!!')
        getinfo()
    #password = '\'' +password+ '\''
    return user_id,password

def login():
    user_id,password = getinfo()
    if check_exists(user_id,password):
        list_data(user_id,password)
    else:
        print("Incorrect Credentials")
        login()

def create_account():
    user_id,password = getinfo()
    if check_unique(user_id):
        add_account(user_id,password)#adds account to userlist and creates folder
        list_data(user_id,password)
    else:
        print("Username already exists")
        create_account()

if __name__ == '__main__':
    welcome_screen()

#'data\' folder needs fullpath
