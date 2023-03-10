
import sys
from colorama import just_fix_windows_console
from termcolor import colored

from data_wrangling.src.data_wrangling import DataWrangling
from database.globals import Globals
from database.sql_shell import connect_to_db
from database.update import update_from_dataframe
from research.calculation_parser import populate_research_tables

def update_database():

    dw = DataWrangling(args = sys.argv[1:])                           # use arguments to choose data files and user options (e.g. --debug)
    dw.read_data()                                                    # read data files provided in command line arguments
    tables = dw.create_weekly_calculations_table(return_tables=True)  # now that data file is read into program, get each weekly calculation table

    try:

        no_database : bool = True if int(sys.argv[1:][sys.argv[1:].index("--no_database") + 1]) == 1 else False
    except:
        no_database : bool = False

    if not no_database:
        if (dw.debug):
            print(colored("\nAdding data to the database:", "blue"))

        cxn_engine = connect_to_db("emma_backend", Globals.db_username, Globals.db_password, use_engine=True)
        
        # table : ((week, year), dataframe)
        for table in tables:
            update_from_dataframe(table[1], table[0][0], table[0][1], cxn_engine, allow_missing_values=False, check_participants_exist=True)
            if (dw.debug):
                print("* (Week {}, {}) data added to back-end database.".format(table[0][0], table[0][1]))
        populate_research_tables(tables, cxn_engine)
    else:
        populate_research_tables(tables, None)


if __name__ == "__main__":
    update_database()