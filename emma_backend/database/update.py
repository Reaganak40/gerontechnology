#!/usr/bin/python

""" This python script contains update utilities to modify and add entries to the EMMA Backend database.
"""

# * Modules
import json
import numpy as np
import os
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy import exc as sa_exc
import sys
from pathlib import Path
from colorama import just_fix_windows_console
from termcolor import colored

# Local Imports
try:
    from globals import Globals
    from sql_shell import connect_to_db
except:
    sys.path.append(os.path.realpath(os.path.dirname(__file__)))
    from globals import Globals
    from sql_shell import connect_to_db

try:
    from research.calculation_parser import get_all_participants
except:
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.sys.path.insert(0,parent_dir) 
    from research.calculation_parser import get_all_participants


# ? VSCode Extensions Used:
# ?     - Better Comments
# ?     - autoDocstring

# * Quick Reference =============================================================================
# * update_from_csv         => Updates the database from a csv calculations file.
# * get_dashboard_variables => Gets the dashboard variables defined in dashboard_variables.json
# * update_schema_file      => Checks the dashboard variables json file and updates the SQL
# *                            schema with it.
# * update_schema           => Updates the database calculations table columns given
# *                            updates from the dashboard variables json file.
# * =============================================================================================

TEST_FILE = os.getcwd() + R'\..\data_wrangling\data\output\Week 14, 2022.csv'

ParticipantDataPath = Path(os.path.realpath(os.path.dirname(__file__))).parent.joinpath("research").joinpath("participants").absolute()

# ===================================================================================================================
#   * replace_string was found on stackoverflow
#    Title: my_sql_replace_into function
#    Author: Frank He
#    Date: 1/3/2023
#    Code version: 1.0
#    Availability: https://stackoverflow.com/questions/6611563/sqlalchemy-on-duplicate-key-update/11762400#11762400
# ==================================================================================================================
def mysql_replace_into(table, conn, keys, data_iter):
    """ This is a method function used by pandas to_sql call. This allows upsert
        functionality, a method to deal with duplicate or pre-existing entries.

    Args:
        table (SQLTable): Pandas created SQLTable instance
        conn (MySQL.Connector): Connection to database
        keys (str): Name of column values for table
        data_iter (list()): Values for each column per row
    """
    from sqlalchemy.dialects.mysql import insert

    data = [dict(zip(keys, row)) for row in data_iter]

    stmt = insert(table.table).values(data)
    update_stmt = stmt.on_duplicate_key_update(**dict(zip(stmt.inserted.keys(), stmt.inserted.values())))

    conn.execute(update_stmt)
    conn.commit()


# Last Edit on 1/1/2023 by Reagan Kelley
# Added parameters
def update_from_csv(filename: str, week, year, allow_missing_values=False, check_participants_exist=True):
    """Updates the database from a csv calculations file.

    Args:
        filename (str): The csv file to reference new variable calculations from.
    """
    calculations_table = pd.read_csv(filename)
    update_from_dataframe(calculations_table, week, year, allow_missing_values=allow_missing_values, check_participants_exist=check_participants_exist)

# Last Edit on 3/6/2023 by Reagan Kelley
# Updates add participant according to new participant table schema
def update_from_dataframe(calculations_table : pd.DataFrame, week, year, cxn_engine = None, allow_missing_values=False, check_participants_exist=True, add_undefined_values=False, debug=False):
    """ Updates the calculation table of the database with entries from a dataframe.

    Args:
        calculations_table (pd.DataFrame): A dataset of calculations
        week (int): The Week number for these entries
        year (int): The year number for these values (e.g, 2023)
        allow_missing_values (bool, optional): If true, will fill unprovided columns with NaN values. Defaults to False.
        check_participants_exist (bool, optional): When True, participants in an entry table that are not defined in the Participants table will be added with an 'Unknown Participant' Tag. Defaults to True.
    Raises:
        Exception: Will raise an exception if variables are mismatched, and given parameters for how to deal with them (e.g, allow_missing_values)
    """
    if(cxn_engine is None):
        cxn_engine = connect_to_db("emma_backend", Globals.db_host, Globals.db_username, Globals.db_password, use_engine=True)

    # The following list comprehension changes the data wrangling variable names to proper SQL names.
    # variables = [(SQL Name, Original Name)]
    variables : list(tuple) = [(("v_" + x).replace("-", "_"), x) for x in list(filter(lambda x: x != "participantId", list(calculations_table.columns)))]

    exec_result = cxn_engine.connect().execute(text("SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS where TABLE_NAME = 'Calculations'"))

    # The variables defined in the SQL table
    database_defined_variables = list(filter(lambda x: x != "participant_id" and x != 'week_number' and x != 'year_number', [result[0] for result in exec_result.fetchall()]))

    # the following list comprehension provides all variables needed by the SQL table not present in the calculations table
    # undefined_variables = [(SQL Name)]
    missing_variables : list(str) = [x for x in database_defined_variables if x not in [x[0] for x in variables]]

    # this is all the variables in the calculation table that need to be removed for database entry
    undefined_variables : list(str) = [x for x in variables if x[0] not in database_defined_variables]

    if (len(missing_variables) > 0):
        if not allow_missing_values:
            err_msg = colored("EMMA Data-Wrangling Error: [Flag: !allow_missing_values]. Cannot proceed, these variables are not present in the calculation table: {}".format(missing_variables), "red")
            raise Exception(err_msg)

    if (len(undefined_variables) > 0):
        if not add_undefined_values:
            err_msg = colored("EMMA Data-Wrangling Error: [Flag: !add_undefined_values]. Cannot proceed, these variables are not defined in the database: {}".format(undefined_variables), "red")
            raise Exception(err_msg)
        
        # add missing variables to the database schema
        # Create a list of tuples to define new calculation table columns [(name_of_column, type)]
        update_schema([(x[0], str(calculations_table[x[1]].dtypes)) for x in undefined_variables],
                      cxn_engine.url.host, cxn_engine.url.username, cxn_engine.url.password, debug=debug)
            
    variable_translations : dict(str, str) = dict((y, x) for x, y in variables)

    if(check_participants_exist):
        add_undefined_participants(calculations_table, cxn_engine)

    # Get DataFrame ready for to_sql
    calculations_table.rename(columns= {"participantId" : "participant_id"}, inplace=True)
    calculations_table.rename(columns=variable_translations, inplace=True)
    calculations_table['week_number'] = [week] * calculations_table.shape[0]
    calculations_table['year_number'] = [year] * calculations_table.shape[0]

    # resolve missing values from database by giving those columns NAN values
    calculations_table = calculations_table.reindex(columns = calculations_table.columns.tolist() + missing_variables)


    calculations_table.to_sql('calculations', con=cxn_engine, if_exists='append', method=mysql_replace_into, index=False)

# Last Edit on 12/31/2022 by Reagan Kelley
# Initial Implementation
def add_undefined_participants(calculations_table, cxn_engine):
    """ Looks through a dataframe and any participants not in the participant db table will be added as an Unknown Participant.

    Args:
        calculations_table (pd.DataFrame): A Calculation Table
        cxn (MySQL.Connector): Connection to a mysql database.
    """
    exec_results = cxn_engine.connect().execute(text("SELECT participant_id FROM Participants"))
    defined_participants = [result[0] for result in exec_results.fetchall()]
    undefined_participants = [x for x in calculations_table["participantId"].to_list() if x not in defined_participants]

    # to maintain foreign key integrity, participants not defined will be created with the name 'Unknown Participant'.
    with cxn_engine.begin() as connection:
        for participant_id in undefined_participants:
            connection.execute(text("INSERT INTO Participants (participant_id, participant_name, study, cohort, active) VALUES({}, 'UnknownParticipant', NULL, NULL, NULL)".format(participant_id)))

# Last Edit on 12/30/2022 by Reagan Kelley
# Initial Implementation
def update_schema(new_calculation_variables, host, username, password, debug=False):
    """ Updates the database calculations table columns given
        with new columns to add to the table schema.

    Args:
        force_delete (bool, optional): When true, will drop columns from the calculation table
        if those columns are no longer defined in dashboard variables. Defaults to False, to avoid accidental deletions.
    """
    cxn = connect_to_db("emma_backend", host, username, password, create=True)

    cursor = cxn.cursor()

    type_dict = {'float64' : 'FLOAT', 'int64' : 'INT'}
    for var_name, var_type in new_calculation_variables:
        
        try:
            var_type = type_dict[var_type]
        except:
            err_msg = colored(f"EMMA Data-Wrangling Error: {var_type} is not a known variable type for update_schema.", "red")
            raise Exception(err_msg)
        
        sql_str = "ALTER TABLE Calculations Add {} {};".format(var_name, var_type)
        cursor.execute(sql_str)
            
    
    if(debug):
        print(f"* Updated Calculation table schema: {len(new_calculation_variables)} new variables added.")
        
    cxn.commit()

def add_participants_from_file(absolute_path : str, cxn_engine = None):
    extension = absolute_path.split(".")[1]

    if extension == "csv":
        participant_table = pd.read_csv(absolute_path)
    elif extension == "xlsx":
        participant_table = pd.read_excel(absolute_path)
    else:
        raise Exception(extension, "is not a valid extension to read.")

    if(cxn_engine is None):
        cxn_engine = connect_to_db("emma_backend", Globals.db_username, Globals.db_password, use_engine=True)
    
    participant_table.dropna(inplace=True)
    print(participant_table)
    participant_table.to_sql('participants', con=cxn_engine, if_exists='append', method=mysql_replace_into, index=False)

def add_participants_from_df(participant_table : pd.DataFrame, cxn_engine = None):
    if(cxn_engine is None):
        cxn_engine = connect_to_db("emma_backend", Globals.db_username, Globals.db_password, use_engine=True)
    
    participant_table.to_sql('participants', con=cxn_engine, if_exists='append', method=mysql_replace_into, index=False)
    
def add_participants_from_research(cxn_engine = None):
    if(cxn_engine is None):
        cxn_engine = connect_to_db("emma_backend", Globals.db_host, Globals.db_username, Globals.db_password, use_engine=True)
    
    participants = get_all_participants()
    add_participants_from_df(participants, cxn_engine)

if __name__ == "__main__":
    add_participants_from_research()