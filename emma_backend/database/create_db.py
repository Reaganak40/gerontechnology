#!/usr/bin/python

""" This script creates the emma backend database if it does not exist,
    and creates the tables according to the local schema.
"""
# * Modules
from mysql.connector import Error
import mysql.connector

# Local Imports
from sql_shell import connect_to_db
from update import *

# ? VSCode Extensions Used:
# ?     - Better Comments
# ?     - autoDocstring

# * Quick Reference =============================================================================
# * create_db               => Creates the EMMA Backend database if it does not exist.
# * executeScriptsFromFile  => Utility function that takes a valid mySQL connection, 
# *                            and executes the SQL scripts from a provided file.
# * =============================================================================================

def create_db():
    """ Creates the EMMA Backend database if it does not exist.
    """
    cxn = connect_to_db("emma_backend", user="root", password="root", create=True)
    executeScriptsFromFile("EMMA_variables_schema.sql", cxn)

def executeScriptsFromFile(filename : str, cxn : mysql.connector.MySQLConnection ):
    """Utility function that takes a valid mySQL connection, 
       and executes the SQL scripts from a provided file.
    Args:
        filename (str): The filename of the sql schema
        cxn (mysql.connector.MySQLConnection): An already established connection with the database.
    """
    cursor = cxn.cursor()

    fd = open(filename, 'r')
    sqlFile = fd.read()
    fd.close()
    sqlCommands = sqlFile.split(';')

    for command in sqlCommands:
        try:
            if command.strip() != '':
                cursor.execute(command)
        except Error as msg:
            print(msg)

    cxn.commit()

def create_and_fill():
    create_db()
    add_participants_from_research()

if __name__ == "__main__":
    create_and_fill()