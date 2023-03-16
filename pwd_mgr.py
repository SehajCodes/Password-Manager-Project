from cryptography.fernet import Fernet
import pandas as pd
import csv
import os
import base64


master_password = None
if not os.path.isfile('./key.txt'):

    print('master password does not exist')
    print('Create a master password')
    master_password = input('Enter new master password: ')

    # make master_password 32 bytes long (required for Fernet)
    master_password = master_password + '1' + '0' * (31 - len(master_password))
    # base64 encode master_password (required for Fernet)
    master_password_encoded = base64.b64encode(master_password.encode())
    # create Fernet object (to encrypt master_password)
    f = Fernet(master_password_encoded)
    # encrypt master_password
    encrypted_master_password = f.encrypt(master_password.encode())
    # save encrypted master_password to key.txt
    with open('./key.txt', 'w') as file:
        file.write(encrypted_master_password.decode())
    print('master password created')

# create an empty passwords.csv file if it does not exist
if not os.path.isfile('./passwords.csv'):
    with open('passwords.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['website', 'username', 'password'])

# ask user for master password, decrypt it and compare it to the one in the txt file
password_attempts = 3
while password_attempts > 0:
    master_password = input('Enter master password: ')
    # make master_password 32 characters long by adding zeros
    master_password = master_password + '1' + '0' * (31 - len(master_password))
    # base64 encode master_password
    master_password_encoded = base64.b64encode(master_password.encode())
    f = Fernet(master_password_encoded)

    # read encrypted key from txt file
    with open('./key.txt', 'r') as file:
        encrypted_key = file.read()
        encrypted_key = encrypted_key.encode()

    try:
        decrypted_master_password = f.decrypt(encrypted_key).decode()
    except Exception as e:
        print('Wrong password')
        password_attempts -= 1
        continue
    if master_password == decrypted_master_password:
        print('Correct password')
        break
# quit if password_attempts == 0
if password_attempts == 0:
    quit()


def add_password():
    # ask user for website, username and password
    print('-'*25)
    website = input('Enter website: ')
    username = input('Enter username: ')
    password = input('Enter password: ')
    print('-'*25)
    encrypted_password = f.encrypt(password.encode()).decode()
    # save password to the csv file
    with open('./passwords.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([website, username, encrypted_password])
    print('Password saved')
    print('-'*25)
    input('Press enter to continue')

def view_password():
        # list index, websites and usernames from csv file and ask user to choose one
        df = pd.read_csv('./passwords.csv')
        if df.empty:
            print('No passwords saved')
            print('-'*25)
            input('Press enter to continue')
        else:
            # show index, website and username columns
            print('-'*25)
            print(df[['website', 'username']])
            print('-'*25)

            # ask user to choose a website index
            website_index = int(input('Enter index: '))
            print('-'*25)
            # get the website and username from the chosen index
            website = df['website'][website_index]
            username = df['username'][website_index]
            # get the encrypted password from the chosen index
            encrypted_password = df['password'][website_index]
            # decrypt the password
            decrypted_password = f.decrypt(encrypted_password).decode()
            # print the website, username and password
            print(f'Website: {website}')
            print(f'Username: {username}')
            print(f'Password: {decrypted_password}')
            print('-'*25)
            input('Press enter to continue')

def delete_password():
    # list index, websites and usernames from csv file and ask user to choose one
    df = pd.read_csv('./passwords.csv')
    # show index, website and username columns
    print('-'*25)
    print(df[['website', 'username']])
    print('-'*25)

    # ask user to choose a website index
    website_index = int(input('Enter index: '))
    print('-'*25)
    # get the website and username from the chosen index
    website = df['website'][website_index]
    username = df['username'][website_index]
    # get the encrypted password from the chosen index
    encrypted_password = df['password'][website_index]
    # decrypt the password
    decrypted_password = f.decrypt(encrypted_password).decode()
    # print the website, username and password
    print(f'Website: {website}')
    print(f'Username: {username}')
    print(f'Password: {decrypted_password}')
    print('-'*25)
    # ask user if they want to delete the password
    delete = input('Delete this password? (y/n): ')
    if delete == 'y':
        # delete the password from the csv file
        df = df.drop(website_index)
        df.to_csv('./passwords.csv', index=False)
        print('Password deleted')
    else:
        print('Password not deleted')
    print('-'*25)
    # wait for user to press enter
    input('Press enter to continue')

while True:
    print('-'*25)
    print('1. Add new password')
    print('2. View password')
    print('3. Delete password')
    print('4. Exit')
    print('-'*25)
    choice = input('Enter your choice: ')
    if choice == '1':
        add_password()
    elif choice == '2':
        view_password()
    elif choice == '3':
        delete_password()
    elif choice == '4':
        break
    else:
        print('Invalid choice')
        print('-'*25)
        input('Press enter to continue')