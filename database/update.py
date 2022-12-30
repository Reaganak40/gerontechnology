#!/usr/bin/python

import pandas as pd
import json


TEST_FILE = R"C:\dev\Gerontechnology\data wrangling\data\output\Week 14, 2022.csv"


def update_from_csv(filename):
    calculations_table = pd.read_csv(filename)
    print(calculations_table)

def get_dashboard_variables():
    with open("dashboard_variables.json") as json_file:
        data = json.load(json_file)
        return data['Variables']


def update_schema_file():
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

def update_schema():
    #update_schema_file()

    variables = [d["name"] for d in get_dashboard_variables()]
    print(variables)


if __name__ == "__main__":
    #update_from_csv(TEST_FILE)
    update_schema()
