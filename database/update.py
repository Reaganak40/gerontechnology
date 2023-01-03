#!/usr/bin/python

""" This python script contains update utilities to modify and add entries to the EMMA Backend database.
"""

# * Modules
import json
import numpy as np
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy import exc as sa_exc
import warnings

# Local Imports
from globals import Globals
from sql_shell import connect_to_db

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

TEST_FILE = R"C:\dev\Gerontechnology\data wrangling\data\output\Week 14, 2022.csv"

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
    from sqlalchemy.ext.compiler import compiles
    from sqlalchemy.sql.expression import Insert

    @compiles(Insert)
    def replace_string(insert, compiler, **kw):
        s = compiler.visit_insert(insert, **kw)
        s = s.replace("INSERT INTO", "REPLACE INTO")
        return s

    data = [dict(zip(keys, row)) for row in data_iter]

    # ! Leads to SAWarning -> Better Solution Encouraged
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=sa_exc.SAWarning)
        conn.execute(table.table.insert(replace_string=""), data)

# Last Edit on 1/1/2023 by Reagan Kelley
# Added parameters
def update_from_csv(filename: str, week, year, allow_missing_values=False, check_participants_exist=True):
    """Updates the database from a csv calculations file.

    Args:
        filename (str): The csv file to reference new variable calculations from.
    """
    calculations_table = pd.read_csv(filename)
    update_from_dataframe(calculations_table, week, year, allow_missing_values=allow_missing_values, check_participants_exist=check_participants_exist)

# Last Edit on 1/3/2023 by Reagan Kelley
# Added Upsert functionality for calculation rows
def update_from_dataframe(calculations_table : pd.DataFrame, week, year, allow_missing_values=False, check_participants_exist=True):
    """ Updates the calculation table of the database with entries from a dataframe.

    Args:
        calculations_table (pd.DataFrame): A dataset of calculations
        week (int): The Week number for these entries
        year (int): The year number for these values (e.g, 2023)
        allow_missing_values (bool, optional): If true, will fill unprovided columns with NaN values. Defaults to False.
        check_participants_exist (bool, optional): When True, participants in an entry table that are not defined 
                                                   in the Participants table will be added with an 'Unknown Participant' Tag. Defaults to True.
    Raises:
        Exception: Will raise an exception if variables are mismatched, and given parameters for how to deal with them (e.g, allow_missing_values)
    """
    cxn = connect_to_db("emma_backend", user="root", password="root", create=True)
    cursor = cxn.cursor()

    # The following list comprehension changes the data wrangling variable names to proper SQL names.
    # variables = [(SQL Name, Original Name)]
    variables : list(tuple) = [(("v_" + x).replace("-", "_"), x) for x in list(filter(lambda x: x != "participantId", list(calculations_table.columns)))]

    cursor.execute("SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS where TABLE_NAME = 'Calculations'")

    # The variables defined in the SQL table use in the dashboard
    database_defined_variables = list(filter(lambda x: x != "participant_id" and x != 'week_number' and x != 'year_number', [result[0] for result in cursor.fetchall()]))

    # the following list comprehension provides all variables needed by the SQL table not present in the calculations table
    # undefined_variables = [(SQL Name)]
    undefined_variables : list(str) = [x for x in database_defined_variables if x not in [x[0] for x in variables]]

    if(not allow_missing_values):
        if (len(undefined_variables) > 0):
            raise Exception("Cannot proceed, these variables are not present in the calculation table: {}".format(undefined_variables))

    variable_translations : dict(str, str) = dict((y, x) for x, y in variables)

    if(check_participants_exist):
        add_undefined_participants(calculations_table, cxn)

    # Get DataFrame read to to_sql
    calculations_table.rename(columns= {"participantId" : "participant_id"}, inplace=True)
    calculations_table.rename(columns=variable_translations, inplace=True)
    calculations_table['week_number'] = [week] * calculations_table.shape[0]
    calculations_table['year_number'] = [year] * calculations_table.shape[0]

    for uv in undefined_variables:
        calculations_table[uv] = [np.nan] * calculations_table.shape[0]

    connection_str = "mysql://{}:{}@localhost/emma_backend".format(Globals.db_username, Globals.db_username)
    engine = create_engine(connection_str)
    engine.connect()

    calculations_table.to_sql('calculations', con=engine, if_exists='append', method=mysql_replace_into, index=False)

# Last Edit on 12/31/2022 by Reagan Kelley
# Initial Implementation
def add_undefined_participants(calculations_table, cxn):
    """ Looks through a dataframe and any participants not in the participant db table will be added as an Unknown Participant.

    Args:
        calculations_table (pd.DataFrame): A Calculation Table
        cxn (MySQL.Connector): Connection to a mysql database.
    """
    cursor = cxn.cursor()
    cursor.execute("SELECT participant_id FROM Participants")
    defined_participants = [result[0] for result in cursor.fetchall()]
    undefined_participants = [x for x in calculations_table["participantId"].to_list() if x not in defined_participants]

    # to maintain foreign key integrity, participants not defined will be created with the name 'Unknown Participant'.
    for to_define in undefined_participants:
        cursor.execute("INSERT INTO Participants (participant_id, first_name, last_name) VALUES({}, 'Unknown', 'Participant')".format(to_define))

    cxn.commit()

# Last Edit on 12/30/2022 by Reagan Kelley
# Initial Implementation
def get_dashboard_variables():
    """Gets the dashboard variables defined in dashboard_variables.json

    Returns:
        List(dict): A list of dictionaries that is [{"name":str, "type":str}]
    """
    with open("dashboard_variables.json") as json_file:
        data = json.load(json_file)
        return data['Variables']

# Last Edit on 12/30/2022 by Reagan Kelley
# Initial Implementation
def update_schema_file():
    """ Updates the schema sql file that is referenced by create_db()
    """
    variable_schema = get_dashboard_variables()
    variables = ""

    for variable in variable_schema:
        variables += "{} {},\n    ".format(variable["name"], variable["type"])

    sql_schema = """\
-- EMMA Variables SCHEMA
-- Last Modified By: Reagan Kelley

CREATE TABLE IF NOT EXISTS Participants
(
    participant_id INTEGER,
    first_name varchar(256),
    last_name varchar(256),

    PRIMARY KEY (participant_id)
);

CREATE TABLE IF NOT EXISTS Calculations
(
    participant_id INTEGER,
    week_number INTEGER,
    year_number INTEGER,

    -- Variables Used in the Calculations Table
    """ + f"{variables}" + """
    PRIMARY KEY (participant_id, week_number, year_number),
    FOREIGN KEY (participant_id) REFERENCES Participants(participant_id)
);
    """

    with open("EMMA_variables_schema.sql", "w") as fd:
        fd.write(sql_schema)

# Last Edit on 12/30/2022 by Reagan Kelley
# Initial Implementation
def update_schema(force_delete=False, debug=False):
    """ Updates the database calculations table columns given
        updates from the dashboard variables json file.

    Args:
        force_delete (bool, optional): When true, will drop columns from the calculation table
        if those columns are no longer defined in dashboard variables. Defaults to False, to avoid accidental deletions.
    """
    update_schema_file()

    variables = get_dashboard_variables()
    variable_names = [d["name"] for d in variables]
    cxn = connect_to_db("emma_backend", user="root", password="root", create=True)

    cursor = cxn.cursor()

    cursor.execute("SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS where TABLE_NAME = 'Calculations'")
    results = [result[0] for result in cursor.fetchall()]

    # exclude any column names that are not variables
    already_defined_variables = list(filter(lambda x: x != "participant_id" and x != 'week_number' and x != 'year_number', results))
    
    extra_variables = [x for x in variables if x["name"] not in already_defined_variables]
    variables_to_drop = [x for x in already_defined_variables if x not in variable_names]

    if(debug):
        print("Variables added: {}".format(extra_variables))
        print("Variables removed: {}".format(variables_to_drop))

    for variable in extra_variables:
        sql_str = "ALTER TABLE Calculations Add {} {};".format(variable["name"], variable["type"])
        cursor.execute(sql_str)
    if(force_delete):
        for variable in variables_to_drop:
            sql_str = "ALTER TABLE Calculations DROP COLUMN {};".format(variable)
            cursor.execute(sql_str)
    
    cxn.commit()

if __name__ == "__main__":
    update_from_csv(TEST_FILE, 14, 2022, allow_missing_values=True)
    #update_schema(force_delete=True, debug=True)
