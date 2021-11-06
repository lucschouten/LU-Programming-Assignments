#For the connection to the MYSQL database
import mysql
from mysql.connector import Error 
#For the encrypting of the passwords
import hashlib
import os

#Make sure you always disconnect after using the database, the database is a free database which only allows for limited open connections.
class Database(object):
    
    def __init__(self, host: str, username:str, password:str, databasename:str)-> None:
        """Initializes the global variables of the database object"""

        self.host = host
        self.username = username
        self.password = password
        self.databasename = databasename
        self.connect()

    def connect(self)-> bool:
        """Starts the connection to the specified database. 

        With theglobal variables host, user, password, and the name of the database created when making the database object, this function starts a connection to the database. 
        
        Returns True when the connection is established otherwise returns False. """
        self.db = mysql.connector.connect(host =f"{self.host}", user = f"{self.username}", password = f"{self.password}", database = f"{self.databasename}")
        if self.db.is_connected:
            print('Connected to the database')
            return True
        else:
            print('Failed to connect to the database')
            return False
    
    def disconnect(self)-> None:
        """ Disconnects from the database."""
        if self.db.is_connected:
            print("closing")
            self.db.close()

    def create_account(self, username: str, password: str)->None:
        """ Creates an account and saves it in the database.

        This functions checks first if the username (can be found in the database) exists.
        When the username doesn't exist yet, it calls a function that creates a random bytearray of 32 bytes, and makes a hash of the password and bytearray together.
        This bytearray and hash then gets saved by sending a query with this information to the database.

        Args: 
            username: the username of the player that creates the account.
            password: the password of the player that creates the account. """

        if self.check_existing_account(username) == False:
            print("Account doesn't exist in database")
            unique_salt = self.generate_unique_salt()
            hexed_salt = unique_salt.hex()
            hash_key = self.hash_password(password,unique_salt)
            hexed_hash_key = hash_key.hex()
            if hash_key != None:
                cursor = self.db.cursor()
                cursor.execute(f'INSERT INTO Account(username) VALUES("{username}");')
                cursor.execute(f'INSERT INTO Password(username, hash_key, salt) VAlUES ("{username}","{hexed_hash_key}","{hexed_salt}");')
                self.db.commit()
                cursor.close()
                print("Account succesfully created")
            else:
                print("Problems with registering")
        else:
            print("This account already exists in the database, please change the username")#Foutmelding
            return "This account already exists in the database, please change the username"
    
    def check_existing_account(self,username: str)-> bool:
        """ Sends a query to the database to check if there is already an existing account. 

        This function sends a query to the database which returns all accounts that have a specified username. 
        The username is the primary key of the account table in the database and is therefore unique. 
        When the len(account_data) > 0 the database returned a row, which means that there exists already an account with the given username.
        
        Args:
            username: the username given by the player."""

        query = f"SELECT username FROM Account WHERE username = '{username}';"
        cursor = self.db.cursor()
        cursor.execute(query)
        account_data = list()
        for data in cursor:
            account_data.append(data)
        cursor.close()
        if len(account_data) > 0:
            return True
        else:
            print("Account not found in database")
            return False

    def check_password(self, username:str, password:str)-> bool or str:
        """checks if the password hashed together with the unique bytearray (salt) can calculate the hash_key. 

        This function retrieves the bytearray and hash from the database based on the specified username.
        It then hashes the password with the retrieved bytearray, if this hash is equal to the hash retrieved from the database the given password is correct.
        This function returns 'True' if the hash_key can be calculated with the given password and returns a message if otherwise.
        
        Args:
            username: the username given by the player.
            password: the password given by the player."""

        if self.check_existing_account(username) == True:
            query = f"SELECT salt, hash_key FROM Password WHERE username = '{username}';"
            cursor = self.db.cursor()
            cursor.execute(query)
            salt_hashkey = list()
            for data in cursor:
                salt_hashkey.append(data)
            cursor.close()
            hexed_salt = salt_hashkey[0][0]
            hexed_hash_key = salt_hashkey[0][1]
            salt = bytes.fromhex(hexed_salt)
            hash_key = bytes.fromhex(hexed_hash_key)
            hashed_password = self.hash_password(password,salt)
            #print(hashed_password)
            if hashed_password == hash_key:
                print('Acces granted')
                return True
            else:
                return "No Acces granted, password didnt match"
        else:
            return "Account not found in database"


    def retrieve_score(self, username: str, password: str, category:str) -> list or str:
        """ Sends a query to the database to retrieve the account information (score).

        This functions returns the account score for a specified category from the database.
        
        Args: 
            username: the username given by the player.
            password: the password given by the player.
            category: the category for which it has to retrieve the score, can be easy/medium/hard/extreme. """

        if self.check_password(username, password) == True:
            query = f"SELECT username, score_{category} FROM Account WHERE username = '{username}';"
            cursor = self.db.cursor()
            cursor.execute(query)
            account_data = list()
            for data in cursor:
                account_data.append(data)
            cursor.close()
            if len(account_data) > 0:
                return account_data
            else:
                print("Account not found in database")
                return "Account not found in database"
        else:
            print('Password is incorrect')


    def updatescore(self, username: str, password: str, category:str, score: int)-> None: 
        """Updates the score for an account based for a specified category.

        This function checks if the account based on the username exists, and authorizes the player by checking if the password belonging to the account is correct.
        This function is a method that send a query to the database to update the score based on the given username, password and score category.

        Args:
            username: the username given by the player.
            password: the password given by the player.
            category: the category based on the category the player has played
            score: the new assigned score."""

        if self.check_existing_account(username) == True:
            if self.check_password(username,password) == True:
                query = f"UPDATE Account SET score_{category} = {score} WHERE username = '{username}';"
                cursor = self.db.cursor()
                cursor.execute(query)
                self.db.commit()
                cursor.close()
                print("Score succesfully updated")
            else:
                print('Cant be updated because password is incorrect')
        else:
            print("Account can't be updated because it does not exist")
    
    def getleaderboard(self, amount: int, category: str)-> list:
        """ Retrieves the data for leaderboard with the highest scores.

        This function sends a query to the database which selects usernames and best scores of the player base based on a specified amount and category.
        It returns an ordered list with the leaderboard information.
        
        Args:
            amount: the amount of player scores which will be returned.
            category: the category of the scores that will be returned: easy/medium/hard/extreme."""

        query = f"SELECT username, score_{category} FROM Account ORDER by score_{category} DESC LIMIT {amount};"
        cursor = self.db.cursor()
        cursor.execute(query)
        leaderboard = list()
        for data in cursor:
            leaderboard.append(data)
        cursor.close()
        print(leaderboard)
        return leaderboard

    def generate_unique_salt(self)-> bytes:
        """Generates a unique bytearray of 32bytes, that can be used to hash the password.

        This function sends a query to the database to check if the randomly generaty bytearray is indeed unique.
    
        It then returns a fully random bytearray """

        random_salt = os.urandom(32) # generates a fully random byte array of 32bytes, not pseudo random (input is number of bytes)
        hex_salt = random_salt.hex()# hexes the bytearray into a string, to store it in the database
        query = f'SELECT * FROM Password WHERE salt = "{hex_salt}";'
        cursor = self.db.cursor()
        cursor.execute(query)
        datalist = list()
        for data in cursor:
            datalist.append(data)
        while len(datalist) > 0:
            random_salt = os.urandom(32) #generates a fully random byte array of 32bytes, not pseudo random (input is number of bytes)
            hex_salt = random_salt.hex() #hexes the byte array into a string
            cursor = self.db.cursor()
            cursor.execute(query)
            datalist.clear()
            for data in cursor:
                datalist.append(data)
        return random_salt

    def hash_password(self, password:str, salt:bytes) -> str:
        """ Hashes the password.

        This funciton hashes the given password with the unique bytearray (salt).
        It returns a hash.
        
        Args:
            password: the password given by the player.
            salt: a random unique bytearray of 32 bytes, generated by the generate_unique_salt function""" 

        hash_key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt,100000,dklen=128) #128byte key
        return hash_key

#db1 = Database("db4free.net", "lucschouten","trivia1234","triviadatabase") #Free database from db4.free.net

#print(db1.retrieve_account("luc","123"))
#db1.create_account("luc1","schouten")
#db1.check_password("dylan", "macquine")
#db1.getleaderboard(3,'easy')

#print(db1.retrieve_score('dylan','macquine','medium')[0][1])
#print(new_score)
#db1.updatescore('dylan','macquine','easy',new_score)

# print(db1.hash_new_password("Test"))
#db1.disconnect() #Deze altijd laten staan.
