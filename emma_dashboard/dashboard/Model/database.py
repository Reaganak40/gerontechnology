#!/usr/bin/python

""" Contains Database class to work with the Emma Backend
"""

from sqlalchemy import engine
import pandas as pd
import numpy as np

class Database():

    def __init__(self, db_engine : engine.Engine):
        self.db = db_engine
        
        with self.db.connect() as connection:
            result = connection.execute("SELECT DATABASE()")
            self.name : str = list(result)[0][0]

    def query_calculation_table(self) -> pd.DataFrame:
        with self.db.connect() as connection:
            return pd.read_sql("SELECT participant_id, week_number, year_number FROM calculations", connection)
    
    def get_users(self) -> pd.DataFrame:
        with self.db.connect() as connection:
            df = pd.read_sql('SELECT * FROM PARTICIPANTS', connection)
            return df.replace(to_replace='None', value=np.nan).dropna()
