
# * Imports
import csv
from colorama import just_fix_windows_console
from datetime import datetime, timedelta
import numpy as np
import os
import pandas as pd
import sys
from termcolor import colored

class Utils:
    # Last Edit on 12/7/2022 by Reagan Kelley
    # Originally written from EMMA_data_wrangling.ipynb
    def next_sunday(original_datetime):
        """Returns the date of the next Sunday relative to the given date.

        Args:
            original_datetime (Datetime): A date

        Returns:
            Datetime: This will be a Sunday datetime.
        """
        days_left = 7 - (original_datetime.floor(freq='D').day_of_week + 1) # offset needed because day of week starts on monday
        if(days_left == 0):
            days_left = 7
        return (pd.to_datetime(original_datetime) + timedelta(days=days_left)).floor(freq='D')

    # Last Edit on 12/7/2022 by Reagan Kelley
    # Originally written from EMMA_data_wrangling.ipynb
    def filter_to_distinct_interactions(df):
        return df

    # Last Edit on 12/7/2022 by Reagan Kelley
    # Originally written from EMMA_data_wrangling.ipynb
    def filter_to_day_of_week(df, day=0):
        """Filters and creates a new DataFrame of interactions that only includes entries of the given day of the week. 
        Precondition: DataFrame only includes a week's worth set of data.

        Args:
            df (DataFrame): At most a week's worth of interactions
            day (int, optional): Discriminates further on query to only when its this day of the week (Sunday = 0, Saturday = 6), Defaults to 0.
        """
        # Filter df to only include interactions on this day of the week
        end_date = Utils.next_sunday(df['timestamp_local'].max()) - timedelta(days=(6-day))
        start_date = end_date - timedelta(days=1)
        new_df = df.loc[(df["timestamp_local"] >= start_date) & (df["timestamp_local"] < end_date)]
        return new_df

class DataWrangling:
    # Last Edit on 12/7/2022 by Reagan Kelley
    # Initial implementation
    def __init__(self, args):
        self.INPUT_DIR = os.getcwd() + R'\..\data\input'
        self.OUTPUT_DIR = os.getcwd() + R'\..\data\output'
        self.weekly_dfs = dict()
        self.__read_args(args)

    # Last Edit on 12/7/2022 by Reagan Kelley
    # Initial implementation
    def __read_args(self, args):
        """Takes command line arguments to setup all parameters or variables for data wrangling.

        Args:
            args (string[]): Contains each argument and parameter in the CLI command.
        """
        try:
            debug_index = args.index("--debug") + 1
            if int(args[debug_index]) == 1:
                self.debug = True
            else:
                self.debug = False
        except:
            self.debug = False
        
        try:
            infile_index = args.index("--input") + 1                    # the argument after --input will be the file that gets read
            self.INFILE = self.INPUT_DIR + RF"\{args[infile_index]}"   
        except:
            self.INFILE = None
            if(self.debug):
                print(colored("WARNING: No file given for data wrangling! (use --input filename)", 'red'))


    # Last Edit on 12/7/2022 by Reagan Kelley
    # Originally written from EMMA_data_wrangling.ipynb
    def participant_dict_to_csv(self, participants, outfile_name="output.csv"):
        """Given an instantiated dictionary, converts to a DataFrame to then be translated to a csv file.

        Args:
            participants (Dict): Participant data, key = participantID, value = dict of variables
            outfile_name (str, optional): The name of the file to be write to. Relative path, using global OUTPUT_DIR. Defaults to "output.csv".
        """
        interactions_df = pd.DataFrame.from_dict(participants, orient='index')
        interactions_df.reset_index(inplace=True)
        interactions_df.rename({'index':'participantId'}, axis='columns', inplace=True)
        interactions_df.to_csv(self.OUTPUT_DIR + "\\{}".format(outfile_name), index=False)

    # Last Edit on 12/7/2022 by Reagan Kelley
    # Originally written from EMMA_data_wrangling.ipynb
    def get_interaction_counts(self, df, elementIDs, day_of_week=-1, distinct=False):
        """Given a DataFrame which contains participant interactions,
        returns a count of interactions for given elementIDs for each participant.

        Args:
            df (Pandas DataFrame): Created earlier from read_excel
            elementIDs (list): A list of elementIDs where each elementID number is to be aggregated.
            day_of_week (int, optional): Discriminates further on query to only when its this day of the week (Sunday = 0, Saturday = 6)
            distinct (bool, optional): Allows us to filter the dataset further to only count distinct uses (5 minute intervals). Defaults to False.
        """
        query_string = ""

        # Filter the Dataset to only include rows from the given day of the week.
        if(day_of_week >= 0):
            df = Utils.filter_to_day_of_week(df, day_of_week)
        
        # Filter the Dataset to only include rows that are distinct uses.
        if(distinct):
            df = Utils.filter_to_distinct_interactions(df)    

        # create a SQL string to filter DataFrame to only include rows with the desired interaction elementIDs
        for i in range(len(elementIDs)):
            query_string += 'elementId == {}'.format(elementIDs[i])
            if((i+1) < len(elementIDs)):
                query_string += " or "
        
        count = df.query(query_string) # count is a new DataFrame that only includes row entries with the given elementIDs
        grouping1 = count.groupby(['participantId', 'elementId']).size() # groups each elementID to how many times each participant used it.
        
        return grouping1.groupby(['participantId']).sum() # returns the sum of each elementIDs use for each participant

    # Last Edit on 12/7/2022 by Reagan Kelley
    # Originally written from EMMA_data_wrangling.ipynb
    def create_variable(self, participants_dict, interactions_df, variable_name, elementIDs, variable_func, day_of_week=-1, distinct=False):
        """Creates a new variable and calculates it, storing the results for each participant in a dictionary.

        Args:
            participants_dict (Dict): Participant data, key = participantID, value = dict of variables
            interactions_df (DataFrame): An already created DataFrame that is data collected from some excel file
            variable_name (string): Identifier by which this variable is known as.
            elementIDs (list): A list of elementIDs that are counted and summed for this variable.
            variable_func (Lambda Function): Describes how the aggregated count will be calculated, typically division due to weekly or daily averages.
            day_of_week (int, optional): Allows us to filter the dataset further to only look at interactions on a specific day of the week (0 = Sunday to 6 = Saturday). Defaults to -1.
            distinct (bool, optional): Allows us to filter the dataset further to only count distinct uses (5 minute intervals). Defaults to False.

        Returns:
            Dict: An updated dictionary containing the calculated variable for all participants in the dataset, interactions_df
        """
        
        # Each interaction is a pair (participantID, count)
        element_count_list = self.get_interaction_counts(interactions_df, elementIDs, day_of_week=day_of_week, distinct=distinct).iteritems()

        for element_count in element_count_list:
            participant_id = element_count[0]

            if participant_id in participants_dict:
                participants_dict[participant_id][variable_name] = variable_func(element_count[1])
            else:
                participants_dict[participant_id] = dict()
                participants_dict[participant_id][variable_name] = variable_func(element_count[1])
        
        return participants_dict
    
    # Last Edit on 12/7/2022 by Reagan Kelley
    # Originally written from EMMA_data_wrangling.ipynb
    def get_variable_calculations(self, df):
        """Given a dataset of interactions from participants, computes and stores calculation dependent variables to an output file.

        Args:
            interactions_filename (string): Excel file where all interaction data is stored (absolute path)
            data_date_range (int, optional): The range of days by which this data was collected. Defaults to 7 (week's worth of data).
        """
        participants = dict()

        variableNames = ["CalenderUse", "SumTotalCalendarInteractions", "CalendaringGoal", "TodayPageUse-Sunday", "TodayPageUse-Monday", "TodayPageUse-Tuesday",
                        "TodayPageUse-Wednesday", "TodayPageUse-Thursday", "TodayPageUse-Friday", "TodayPageUse-Saturday", "SumTotalEventInteractions", "TodayPageGoal-Sunday",
                        "TodayPageGoal-Monday", "TodayPageGoal-Tuesday", "TodayPageGoal-Wednesday", "TodayPageGoal-Thursday", "TodayPageGoal-Friday", "TodayPageGoal-Saturday",
                        "LTGFolderUse", "SumTotalLTGNoteInteractions", "LTGGoal", "FZFolderUse", "SumTotalFZNoteInteractions", "FZGoal"]

        participants = self.create_variable(participants, df, "CalenderUse", [9], lambda x: x/(7))
        participants = self.create_variable(participants, df, "SumTotalCalendarInteractions", [9, 18, 19, 20], lambda x: x/(7))
        participants = self.create_variable(participants, df, "CalendaringGoal", [9], lambda x: x/(4))

        participants = self.create_variable(participants, df, "TodayPageUse-Sunday",    [8, 13, 379, 380, 381, 384], lambda x: x, day_of_week=0, distinct=True)
        participants = self.create_variable(participants, df, "TodayPageUse-Monday",    [8, 13, 379, 380, 381, 384], lambda x: x, day_of_week=1, distinct=True)
        participants = self.create_variable(participants, df, "TodayPageUse-Tuesday",   [8, 13, 379, 380, 381, 384], lambda x: x, day_of_week=2, distinct=True)
        participants = self.create_variable(participants, df, "TodayPageUse-Wednesday", [8, 13, 379, 380, 381, 384], lambda x: x, day_of_week=3, distinct=True)
        participants = self.create_variable(participants, df, "TodayPageUse-Thursday",  [8, 13, 379, 380, 381, 384], lambda x: x, day_of_week=4, distinct=True)
        participants = self.create_variable(participants, df, "TodayPageUse-Friday",    [8, 13, 379, 380, 381, 384], lambda x: x, day_of_week=5, distinct=True)
        participants = self.create_variable(participants, df, "TodayPageUse-Saturday",  [8, 13, 379, 380, 381, 384], lambda x: x, day_of_week=6, distinct=True)

        participants = self.create_variable(participants, df, "SumTotalEventInteractions", [13, 103, 104, 379, 380, 381, 384], lambda x: x/(7))

        participants = self.create_variable(participants, df, "TodayPageGoal-Sunday",    [13, 103, 104, 379, 380, 381, 384], lambda x: x/(3), day_of_week=0, distinct=True)
        participants = self.create_variable(participants, df, "TodayPageGoal-Monday",    [13, 103, 104, 379, 380, 381, 384], lambda x: x/(3), day_of_week=1, distinct=True)
        participants = self.create_variable(participants, df, "TodayPageGoal-Tuesday",   [13, 103, 104, 379, 380, 381, 384], lambda x: x/(3), day_of_week=2, distinct=True)
        participants = self.create_variable(participants, df, "TodayPageGoal-Wednesday", [13, 103, 104, 379, 380, 381, 384], lambda x: x/(3), day_of_week=3, distinct=True)
        participants = self.create_variable(participants, df, "TodayPageGoal-Thursday",  [13, 103, 104, 379, 380, 381, 384], lambda x: x/(3), day_of_week=4, distinct=True)
        participants = self.create_variable(participants, df, "TodayPageGoal-Friday",    [13, 103, 104, 379, 380, 381, 384], lambda x: x/(3), day_of_week=5, distinct=True)
        participants = self.create_variable(participants, df, "TodayPageGoal-Saturday",  [13, 103, 104, 379, 380, 381, 384], lambda x: x/(3), day_of_week=6, distinct=True)

        # ! Resolve function zone token v. LTG token
        participants = self.create_variable(participants, df, "LTGFolderUse",  [24, 220, 322], lambda x: x/(7), distinct=True)
        participants = self.create_variable(participants, df, "SumTotalLTGNoteInteractions",  [24, 64, 65, 220], lambda x: x/(7))
        participants = self.create_variable(participants, df, "LTGGoal",  [24, 220, 322], lambda x: x)
        participants = self.create_variable(participants, df, "FZFolderUse",  [24, 220, 322], lambda x: x/(7), distinct=True)
        participants = self.create_variable(participants, df, "SumTotalFZNoteInteractions",  [24, 64, 65, 220], lambda x: x/(7))
        participants = self.create_variable(participants, df, "FZGoal",  [24, 220, 322], lambda x: x) # ! this is currently the same as LTGGoal

        # set the values of variables not calculated to 0 (the use of them by the participants never appeared in the dataset)
        for participant_id in participants:
            keys = participants[participant_id].keys()
            undeclared_variables = list(set(variableNames).difference(keys)) # these are the variables for each participant that were not calculated. (=0)
            for variable in undeclared_variables:
                participants[participant_id][variable] = 0
        
        return participants

        
    # Last Edit on 12/7/2022 by Reagan Kelley
    # Initial Implementation
    def read_file(self):
        """Given a csv file, converts a dataset of interactions spanning many weeks into many datasets by week.

        Args:
            interactions_filename (string): Absolute filepath of excel file.

        Returns:
            Dict: Dictionary of interaction DataFrames. Key = StartDate, Value=DataFrame
        """
        if self.debug:
            print(colored("\nReading Interactions from Dataset...", 'blue'))

        if self.INFILE == None:
            raise Exception("INFILE is None")

        # gets the entire dataset from the provided infile.
        interactions_raw = pd.read_excel(self.INFILE)

        # Get the date range in the dataset -> will be used to create weekly dataframes
        start_date = interactions_raw['timestamp_local'].min()  # the earliest entry in the dataset
        end_parsec = Utils.next_sunday(start_date)              # the beginning of the next week
        end_date = interactions_raw['timestamp_local'].max()    # the latest entry in the dataset

        # separate entries by weekly ranges (sunday to saturday)
        while(start_date < end_date):
            df = interactions_raw.loc[(interactions_raw["timestamp_local"] >= start_date) & (interactions_raw["timestamp_local"] < end_parsec)]
            self.weekly_dfs[(start_date.strftime("%U"), start_date.strftime("%Y"))] = df        
            start_date = end_parsec
            end_parsec = Utils.next_sunday(start_date)
        
        if self.debug:
            print("* Results: {} weeks of data gathered.".format(len(self.weekly_dfs)))

        return self.weekly_dfs

    # Last Edit on 12/7/2022 by Reagan Kelley
    # Originally written from EMMA_data_wrangling.ipynb
    def create_weekly_calculations_table(self):
        """Given a large dataset of interactions from multiple participants, outputs all weekly csv files from that data showcasing desired calculated variables.

        Args:
            interactions_filename (string): Absolute path to large dataset
        """
        if self.debug:
            print(colored("\nCalculating Variables for each week...", 'blue'))


        for date, df in self.weekly_dfs.items():
            filename = "Week {}, {}".format(date[0], date[1])  # The Week and Year of the next dataframe that will be used to calculate variables.
            
            if(self.debug):
                print(f"* Calculating variables for ({filename})")
            
            participants = self.get_variable_calculations(df)                          # Get variable calculations for each participant that week
            self.participant_dict_to_csv(participants, "{}.csv".format(filename))      # Output results to the output directory

# Last Edit on 12/7/2022 by Reagan Kelley
# Initial Implementation
def main():
    """Executes data wrangling from the provided command-line arguments
    """
    dw = DataWrangling(args = sys.argv[1:])   # use arguments to choose data file and user options (e.g. debug)
    dw.read_file()                            # read data file provided in command line arguments
    dw.create_weekly_calculations_table()     # now that data file is read into program, output the variable calculations for each week.

if os.name == 'nt':
    just_fix_windows_console()

if __name__ == "__main__":
    main()