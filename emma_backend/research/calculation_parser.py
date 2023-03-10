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

        participants = None
        # get all excel files in the directory, exclude hidden recovery files
        filenames = glob.glob(str(participant_table_path) + "\[!~$]*.xlsx")
        for file in filenames:
            current_participant_table = pd.read_excel(file)
            columns = current_participant_table.columns

            bad_table = False
            for check_column in ["participant_id", "participant_name", "study", "cohort", "active"]:
                if check_column not in columns:
                    print("Warning - Participant Table [{}] ignored because of missing column: {}".format(file.split("\\")[-1], check_column))
                    bad_table = True
                    break
            if bad_table:
                continue

            if participants is None:
                participants = current_participant_table
            else:
                participants = pd.concat([participants, current_participant_table], ignore_index=True).drop_duplicates().reset_index(drop=True)

        print(participants)
        return participants
    return None
        

def populate_research_tables(calculation_tables : list[tuple[tuple[str, str], pd.DataFrame]] , cxn_engine = None):
    participants = get_all_participants(cxn_engine)
    
    for weekly_calculation_table in calculation_tables:
        pass
        # weekly_calculation_table[1] is the dataframe for that week