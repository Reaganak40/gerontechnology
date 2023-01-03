
import sys

from data_wrangling.src.data_wrangling import DataWrangling

def update_database():
    dw = DataWrangling(args = sys.argv[1:])                          # use arguments to choose data files and user options (e.g. --debug)
    dw.read_data()                                                   # read data files provided in command line arguments
    tables = dw.create_weekly_calculations_table(return_tables=True) # now that data file is read into program, get each weekly calculation table

    for table in tables:
        print(len(table[1].columns))

if __name__ == "__main__":
    update_database()