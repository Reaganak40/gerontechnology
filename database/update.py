#!/usr/bin/python

""" This script allows the user to access the backend database directly.
"""

# * Modules
from colorama import just_fix_windows_console
from getpass import getpass
from mysql.connector import Error
import mysql.connector
import os
from termcolor import colored

# ? VSCode Extensions Used:
# ?     - Better Comments
# ?     - autoDocstring

# * Quick Reference =============================================================================
# * connect_to_db   => Prompts for user and password and then when validated connects
# *                    to back-end database
# * sql_shell       => Given a valid connection to a mysql database, can use this shell
# *                    to send sql queries.
# * =============================================================================================

def connect_to_db(database_name : str):
    """ Prompts for user and password and then when validated connects
        to back-end database
    Args:
        database_name (str): The name of the already defined mySQL database.

    Returns:
        mysql.connector.MySQLConnection: A valid connection to the database.
    """
    try:
        cxn = mysql.connector.connect(host="localhost",
                user=input("Enter username: "),
                password=getpass("Enter password: "),
                database=database_name,)
        return cxn
    except Error as e:
        print(e)
        return None

def sql_shell(cxn : mysql.connector.MySQLConnection = None):
    """Given a valid connection to a mysql database, can use this shell
    to send sql queries.

    Args:
        cxn (mysql.connector.MySQLConnection, optional): _description_. Defaults to None.
    """
    if(cxn is not None):
        with cxn.cursor() as cursor:
            connected = True
            while(connected):
                sql_string = input(colored("\n>> ", 'red'))

                if(sql_string == "quit"):
                    connected = False
                else:
                    try:
                        cursor.execute(sql_string)
                        result = cursor.fetchall()
                        for row in result:
                            print(row[0])
                    except Error as e:
                        print(e)
            
            

def main():
    cxn = connect_to_db("testdb")
    sql_shell(cxn)

if os.name == 'nt':
    just_fix_windows_console()

if __name__ == "__main__":
    main()
