#!/usr/bin/python

""" Database is a querying support class that allows model classes to 
get data from the database and cache it for future use.
"""
# * Modules
import pyodbc
import pandas as pd
from config import Config

from sqlalchemy import create_engine
import os

connection_string = "DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};" +\
    "DBQ=" + os.path.join(Config.DB_FOLDER, Config.DB_NAME)

connection = pyodbc.connect(connection_string)

#engine = create_engine("mssql+pyodbc:///" + pyodbc_connection_string)


# =======================================================================
# COMMON SQL QUERIES: Defined here for legibility
# =======================================================================
SQL_QUERY_USERS = r'SELECT * FROM users_t'

# =======================================================================
# =======================================================================

#TODO: Convert to SQL Alchemy
class Database():
    """ Contains utility functions to interact with database data.
    
    Args:
        database_folder (str, optional): Directory location where database files are located. Defaults to Config.DB_FOLDER.
    """

    def __init__(self, database_folder = Config.DB_FOLDER):
        self.database_folder = database_folder

    def get_users():
        users_data = pd.read_sql(SQL_QUERY_USERS, connection)
        return users_data

class DatabaseCache(Database):
    """Provides extended functionality of the Database class, 
    where we can keep data in RAM for quicker retrieval, instead of querying each request.

    Args:
        Database (Parent Class): Inherits all functionality from Database, but when 
        the util functions are called, they are then stored in this instance.
    """
    def __init__(self):
        self.users = None
    
    def get_users(self):
        """Gets a table of users; participants and clinicians.

        Returns:
            Series: A table of users.
        """
        if(self.users is None):
            self.users = super().get_users()
        return self.users