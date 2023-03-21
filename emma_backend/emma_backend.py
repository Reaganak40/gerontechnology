
import sys
from colorama import just_fix_windows_console
from termcolor import colored

from data_wrangling.src.data_wrangling import DataWrangling
from database.globals import Globals
from database.sql_shell import connect_to_db
from database.update import update_from_dataframe
from research.calculation_parser import populate_research_tables

def update_database(calculation_tables, cxn_engine = None, debug : bool = False):
    if (debug):
        print(colored("\nAdding data to the database:", "blue"))

    cxn_engine = connect_to_db("emma_backend", Globals.db_username, Globals.db_password, use_engine=True)
    
    # table : ((week, year), dataframe)
    for table in calculation_tables:
        update_from_dataframe(table[1].copy(), table[0][0], table[0][1], cxn_engine, allow_missing_values=False, check_participants_exist=True)
        if (debug):
            print("* (Week {}, {}) data added to back-end database.".format(table[0][0], table[0][1]))

def update_research(calculation_tables, cxn_engine = None, debug : bool = False):
    if (debug):
        print(colored("\nCreating parsed calculation tables for research studies:", "blue"))
    populate_research_tables(calculation_tables, cxn_engine, debug=debug)


def emma_backend(args):
    dw = DataWrangling(args = args)                                   # use arguments to choose data files and user options (e.g. --debug)
    dw.read_data()                                                    # read data files provided in command line arguments
    tables = dw.create_weekly_calculations_table(return_tables=True)  # now that data file is read into program, get each weekly calculation table

    # * Get Needed Command Line Arguments
    # * no_database => When true, will not use database participant data nor add calculation tables to database
    # * research    => When true, will use participant table (from db or from research/participants/*.xlsx) to update research tables 
    try:
        no_database : bool = True if int(sys.argv[1:][sys.argv[1:].index("--no_database") + 1]) == 1 else False
    except:
        no_database : bool = False
    
    try:
        research : bool = True if int(sys.argv[1:][sys.argv[1:].index("--research") + 1]) == 1 else False
    except:
        research : bool = False
    
    # * Add information to database if requested.
    if not no_database:
        cxn_engine = connect_to_db("emma_backend", Globals.db_username, Globals.db_password, use_engine=True)
    else:
        cxn_engine = None

    # * Add calculation tables to database if requested
    if research:
        update_research(tables, cxn_engine, debug=dw.debug)
    if not no_database:
        update_database(tables, cxn_engine, debug=dw.debug)


if __name__ == "__main__":
    emma_backend(sys.argv[1:])