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
        
        participants.dropna(inplace=True)
        return participants
    
    return pd.read_sql('SELECT * FROM PARTICIPANTS', cxn_engine)

def populate_research_tables(calculation_tables : list[tuple[tuple[str, str], pd.DataFrame]] , cxn_engine = None, debug : bool = False):
    participants = get_all_participants(cxn_engine)
    if (debug):
        print("* {} participants found in {}".format(len(participants), "participant table(s)" if cxn_engine is None else "database"))
    
    data_dir = Path(os.path.realpath(os.path.dirname(__file__))).joinpath('data').absolute()
    if not data_dir.exists():
        data_dir.mkdir()
    
    for date, calculations in calculation_tables:
        weekly_participants = participants[participants['participant_id'].isin(calculations['participantId'])]
        study_options = weekly_participants['study'].unique()
        
        for study in study_options:
            study_participants = participants[participants['study'] == study]
            cohort_options = study_participants['cohort'].unique()
            for cohort in cohort_options:
                cohort_participants = study_participants[(study_participants['cohort'] == cohort) & (study_participants['active'] == 1)]
                parsed_table = calculations[calculations['participantId'].isin(cohort_participants['participant_id'])]

                missing_participants = set(list(cohort_participants['participant_id'])).difference(list(parsed_table['participantId']))
                
                if len(missing_participants) > 0:
                    ct2_dict = {col_name:[0] * len(missing_participants) for col_name in parsed_table.columns}
                    ct2_dict['participantId'] = list(missing_participants)
                    ct2 = pd.DataFrame(ct2_dict)
                    parsed_table = pd.concat([parsed_table, ct2], ignore_index=True)
                    parsed_table.reset_index()
                
                output_dir = data_dir.joinpath(study).joinpath("Cohort {}".format(cohort))
                
                if not output_dir.exists():
                    output_dir.mkdir(parents=True)
                output_dir = output_dir.joinpath("Week {}, {}.csv".format(date[0], date[1]))
                parsed_table.to_csv(output_dir, index=False)
                
                if (debug):
                     print("* Calculation table created for [Study: {}, Cohort: {}] for (Week {}, {})".format(study, cohort, date[0], date[1]))