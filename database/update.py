#!/usr/bin/python

# * Modules
import pandas as pd
import json

# Local Imports
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

def update_from_csv(filename: str):
    """Updates the database from a csv calculations file.

    Args:
        filename (str): The csv file to reference new variable calculations from.
    """
    calculations_table = pd.read_csv(filename)
    print(calculations_table)

def get_dashboard_variables():
    """Gets the dashboard variables defined in dashboard_variables.json

    Returns:
        List(dict): A list of dictionaries that is [{"name":str, "type":str}]
    """
    with open("dashboard_variables.json") as json_file:
        data = json.load(json_file)
        return data['Variables']


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

def update_schema(force_delete=False):
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

    print(extra_variables)
    print(variables_to_drop)

    for variable in extra_variables:
        sql_str = "ALTER TABLE Calculations Add {} {};".format(variable["name"], variable["type"])
        cursor.execute(sql_str)
    if(force_delete):
        for variable in variables_to_drop:
            sql_str = "ALTER TABLE Calculations DROP COLUMN {};".format(variable)
            cursor.execute(sql_str)
    
    cxn.commit()

if __name__ == "__main__":
    #update_from_csv(TEST_FILE)
    update_schema(force_delete=True)
