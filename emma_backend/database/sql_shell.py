#!/usr/bin/python

""" This script allows the user to access the backend database directly.
"""

# * Modules
from colorama import just_fix_windows_console
from getpass import getpass
from mysql.connector import Error
import mysql.connector
import os
from sqlalchemy import create_engine
import sys
from termcolor import colored

try:
    from globals import Globals
except:
    sys.path.append(os.path.realpath(os.path.dirname(__file__)))
    from globals import Globals


# ? VSCode Extensions Used:
# ?     - Better Comments
# ?     - autoDocstring

# * Quick Reference =============================================================================
# * connect_to_db   => Prompts for user and password and then when validated connects
# *                    to back-end database
# * sql_shell       => Given a valid connection to a mysql database, can use this shell
# *                    to send sql queries.
# * =============================================================================================

# Last Edit on 12/30/2022 by Reagan Kelley
# Initial implementation
def connect_to_db(database_name : str, host=None, user=None, password=None, create=False, use_engine=False):
    """ Prompts for user and password and then when validated connects
        to back-end database
    Args:
        database_name (str): The name of the already defined mySQL database.

    Returns:
        mysql.connector.MySQLConnection: A valid connection to the database.
    """
    if(not use_engine):
        try:
            if(not create):
                if(user is not None and password is not None):
                    cxn = mysql.connector.connect(host=host,
                            user=user,
                            password=password,
                            database=database_name
                            )
                else:
                    cxn = mysql.connector.connect(host=host,
                            user=input("Enter username: "),
                            password=getpass("Enter password: "),
                            database=database_name
                            )
            else:
                if(user is not None and password is not None):
                    cxn = mysql.connector.connect(host=host,
                            user=user,
                            password=password,
                            )
                else:
                    cxn = mysql.connector.connect(host=host,
                            user=input("Enter username: "),
                            password=getpass("Enter password: "),
                            )
                cursor = cxn.cursor()
                cursor.execute("CREATE DATABASE IF NOT EXISTS {}".format(database_name))
                cxn.connect(database=database_name)
            return cxn
        except Error as e:
            print(e)
            return None
    else:
        if(user is None or password is None):
            user=input("Enter username: "),
            password=getpass("Enter password: ")
        connection_str = "mysql://{}:{}@{}/{}".format(user, password, host, database_name)
        return create_engine(connection_str, future=True)

# Last Edit on 12/30/2022 by Reagan Kelley
# Initial implementation
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
                    cxn.commit()
                else:
                    try:
                        cursor.execute(sql_string)
                        result = cursor.fetchall()
                        for row in result:
                            print(row)
                    except Error as e:
                        print(e)
            
            
# Last Edit on 12/30/2022 by Reagan Kelley
# Initial implementation
def main():
    cxn = connect_to_db("emma_backend", create=True, host="localhost")
    sql_shell(cxn)

if os.name == 'nt':
    just_fix_windows_console()

if __name__ == "__main__":
    main()
