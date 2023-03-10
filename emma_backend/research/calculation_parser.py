import pandas as pd
import os
import glob
from pathlib import Path


def get_all_participants(cxn_engine = None):
    """Returns a dataframe of all participants who belong to a weekly calculation table, as well
        as those who were active during that time but were omitted

    Args:
        calculation_table (pd.DataFrame): The weekly calculation table
        cxn_engine (mysql.connector.MySQLConnection, optional): A valid connection to the database. Defaults to None.
        When None uses the participant tables in the participants directory.
    """
    if cxn_engine is None:
        participant_table_path = Path(os.path.realpath(os.path.dirname(__file__))).joinpath("participants").absolute()

        if not participant_table_path.exists():
            raise Exception("Looking for directory with participant tables ...\nPath: [{}] does not exist.".format(str(participant_table_path)))

        # get all excel files in the directory, exclude hidden recovery files
        filenames = glob.glob(str(participant_table_path) + "\[!~$]*.xlsx")
        for file in filenames:
            print(pd.read_excel(file))

def populate_research_tables(calculation_tables : list[tuple[tuple[str, str], pd.DataFrame]] , cxn_engine = None):
    participants = get_all_participants(cxn_engine)
    
    for weekly_calculation_table in calculation_tables:
        pass
        # weekly_calculation_table[1] is the dataframe for that week