#!/usr/bin/python

""" Contains Database class to work with the Emma Backend
"""

from sqlalchemy import engine, text
import pandas as pd
import numpy as np

class Database():

    def __init__(self, db_engine : engine.Engine):
        self.db = db_engine
        
        with self.db.connect() as connection:
            result = connection.execute(text("SELECT DATABASE()"))
            self.name : str = list(result)[0][0]

    def query_calculation_table(self) -> pd.DataFrame:
        with self.db.connect() as connection:
            return pd.read_sql(text("SELECT participant_id, week_number, year_number FROM calculations"), connection)
    
    def get_users(self) -> pd.DataFrame:
        with self.db.connect() as connection:
            df = pd.read_sql(text('SELECT * FROM PARTICIPANTS'), connection)
            return df.replace(to_replace='None', value=np.nan).dropna()
    
    def get_user(self, id)  -> pd.DataFrame:
        with self.db.connect() as connection:
            df = pd.read_sql(text('SELECT * FROM PARTICIPANTS WHERE participant_id={}'.format(id)), connection)
            return df.replace(to_replace='None', value=np.nan).dropna()
        
    def get_tables(self, id) -> pd.DataFrame:
        with self.db.connect() as connection:
            df = pd.read_sql(text('SELECT * FROM calculations WHERE participant_id={}'.format(id)), connection)
            return df.replace(to_replace='None', value=np.nan).dropna()