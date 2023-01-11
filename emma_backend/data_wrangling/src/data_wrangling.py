#!/usr/bin/python

""" This program allows us to take in EMMA datasets, a collection of 
    entries of participants who use the EMMA app, and aggregate calculations 
    that are both used in research and in the medical field.
"""
# * Modules
from colorama import just_fix_windows_console
import os
import pandas as pd
import sys
from termcolor import colored


# Local Imports
try:
    from dataset import DatasetType, Dataset
    from utils import Utils
    from variable import create_variable_dictionary, Variable
except:
    sys.path.append(os.path.realpath(os.path.dirname(__file__)))
    from dataset import DatasetType, Dataset
    from utils import Utils
    from variable import create_variable_dictionary, Variable

# ? VSCode Extensions Used:
# ?     - Better Comments
# ?     - autoDocstring

# * Quick Reference =============================================================================
# * Utils           => Contains general helpful functions that goes beyond EMMA data wrangling
# * DatasetType     => Includes enums that is used to identify a provided dataset
# * DataWrangling   => Class that includes all use-cases and execution to create variables
# * Dataset         => Private class object that contains all data and attributes of a dataset
# * =============================================================================================

class DataWrangling:

    # Last Edit on 12/7/2022 by Reagan Kelley
    # Initial implementation
    def __init__(self, args):
        # TODO: Provide absolute and relative path functionality
        
        self.INPUT_DIR = os.path.realpath(os.path.dirname(__file__)) + '/../data/input'
        self.OUTPUT_DIR = os.path.realpath(os.path.dirname(__file__)) + '/../data/output'

        self.__init_token_dict()
        self.data : dict[str, Dataset] = {}
        self.__read_args(args)
        self.variables : dict[str, Variable] = create_variable_dictionary("variable_definitions.json")

        self.variableNames = []
        for key in self.variables.keys():
            self.variableNames.append(key)
    
    # Last Edit on 12/13/2022 by Reagan Kelley
    # Added Event args and verify-integrity
    def __read_args(self, args):
        """Takes command line arguments to setup all parameters or variables for data wrangling.

        Args:
            args (string[]): Contains each argument and parameter in the CLI command.
        """
        # ? Argument Dictionary ==========================================================================================
        # ? --debug            => When true, Prints processes to console throughout the application
        # ? --interactions     => Provided path to interactions excel data
        # ? --events           => Provided path to events excel data
        # ? --verify-integrity => When true, will move bad variable calculations to trash dir
        # ?                       Bad Variable Calculations Are:
        # ?                             * Weekly_dfs with incomplete weeks (missing days - particularly at edge weeks)
        # ?                             * If there is a weekly_df for interactions but not one for events (or vice versa)
        # ? ==============================================================================================================

        # * Debug Options (--debug) => Defaults to False
        try:
            debug_index = args.index("--debug") + 1
            if int(args[debug_index]) == 1:
                self.debug = True
            else:
                self.debug = False
        except:
            self.debug = False
        
        # * Interactions Dataset Options (--interactions) => Defaults to None (this is bad)
        try:
            interactions_infile_index = args.index("--interactions") + 1   # the argument after --interactions will be the file that gets read
            self.data[DatasetType.INTERACTIONS] = Dataset(DatasetType.INTERACTIONS, self.INPUT_DIR + F"/{args[interactions_infile_index]}")
        except:
            self.data[DatasetType.INTERACTIONS] = None
            if(self.debug):
                print(colored("WARNING: No file provided for interactions! (use --interactions filename)", 'red'))
        
        # * Events Dataset Options (--events) => Defaults to None (this is bad)
        try:
            events_infile_index = args.index("--events") + 1              # the argument after --events will be the file that gets read
            self.data[DatasetType.EVENTS] = Dataset(DatasetType.EVENTS, self.INPUT_DIR + F"/{args[events_infile_index]}")
        except:
            self.data[DatasetType.EVENTS] = None
            if(self.debug):
                print(colored("WARNING: No file provided for events! (use --events filename)", 'red'))

        # * Verify Integrity Options (--verify-integrity) => Defaults to False
        try:
            verify_integrity_index = args.index("--verify-integrity") + 1
            if int(args[verify_integrity_index]) == 1:
                self.verify_integrity = True
            else:
                self.verify_integrity = False
        except:
            self.verify_integrity = False

    def __init_token_dict(self):
        self.emma_token = {}

        # Keys provided via EMMA Microsoft Teams
        self.emma_token['LTG'] = '280B85CE-E425-46CA-B4E5-F09933601883'
        self.emma_token['FZ']  = '180B85CE-E425-46CA-B4E5-F09933601773'

    # Last Edit on 12/7/2022 by Reagan Kelley
    # Originally written from EMMA_data_wrangling.ipynb
    def participant_dict_to_csv(self, participants, outfile_name="output.csv"):
        """Given an instantiated dictionary, converts to a DataFrame to then be translated to a csv file.

        Args:
            participants (Dict): Participant data, key = participantID, value = dict of variables
            outfile_name (str, optional): The name of the file to be write to. Relative path, using global OUTPUT_DIR. Defaults to "output.csv".
        """
        self.participant_dict_to_df(participants).to_csv(self.OUTPUT_DIR + "/{}".format(outfile_name), index=False)

    def participant_dict_to_df(self, participants):
        interactions_df = pd.DataFrame.from_dict(participants, orient='index')
        interactions_df.reset_index(inplace=True)
        interactions_df.rename({'index':'participantId'}, axis='columns', inplace=True)

        column_order = self.variableNames.copy()
        column_order.insert(0, 'participantId')
        
        # make sure columns are in the correct order
        interactions_df = interactions_df.loc[:, column_order]
        interactions_df = interactions_df.sort_values(by=['participantId'])
        return interactions_df

    # Last Edit on 12/7/2022 by Reagan Kelley
    # Originally written from EMMA_data_wrangling.ipynb
    def get_interaction_counts(self, df, elementIDs, day_of_week=-1, distinct=False, tokens=[]):
        """ Given a DataFrame which contains participant interactions,
            returns a count of interactions for given elementIDs for each participant.

        Args:
            df (Pandas DataFrame): Created earlier from read_excel
            elementIDs (list): A list of elementIDs where each elementID number is to be aggregated.
            day_of_week (int, optional): Discriminates further on query to only when its this day of the week (Sunday = 0, Saturday = 6)
            distinct (bool, optional): Allows us to filter the dataset further to only count distinct uses (5 minute intervals). Defaults to False.
            tokens (list, optional): A string list of token names that each entry must also have. Defaults to [].

        Returns:
            DataFrame: The variable value for each participant in the df
        """
        query_string = ""

        # Filter the Dataset to only include rows from the given day of the week.
        if(day_of_week >= 0):
            df = Utils.filter_to_day_of_week(df, day_of_week)
        
        # Filter the Dataset to only include rows that are distinct uses.
        if(distinct):
            df = Utils.filter_to_distinct_interactions(df)


        # create a SQL string to filter DataFrame to only include rows with the desired interaction elementIDs
        query_string += "("
        for i in range(len(elementIDs)):
            query_string += 'elementId == {}'.format(elementIDs[i])
            if((i+1) < len(elementIDs)):
                query_string += " or "
        query_string += ")"
        
        # Add to the SQL string to filter DataFrame to only include those elementIDs with these tokens
        if(tokens is not None):
            query_string += " and ("
            for i in range(len(tokens)):
                query_string += "token == '{}'".format(self.emma_token[tokens[i]]) # use emma_token dict to find the alpha-numerical key-value
                if((i+1) < len(tokens)):
                    query_string += " or "
            query_string += ")"

        count = df.query(query_string) # count is a new DataFrame that only includes row entries with the given elementIDs
        grouping1 = count.groupby(['participantId', 'elementId']).size() # groups each elementID to how many times each participant used it.
        
        return grouping1.groupby(['participantId']).sum() # returns the sum of each elementIDs use for each participant

    def get_events_counts(self, df, sum, healthTrackType, completed = False, day_of_week=-1):
        """ Given a DataFrame which contains participant events,
            returns a sum in a column for given healthTrackType for each participant.

        Args:
            df (Pandas DataFrame): Created earlier from read_excel
            count (str): the name of the column in the events table to count.
            healthTrackType (list[str]): Which healthTracking tags to filter by.
            day_of_week (int, optional): Discriminates further on query to only when its this day of the week (Sunday = 0, Saturday = 6)
        Returns:
            DataFrame: The variable value for each participant in the df
        """
        query_string = ""

        # create a SQL string to filter DataFrame to only include rows with the desired interaction elementIDs
        query_string += "("
        for i in range(len(healthTrackType)):
            query_string += "healthTrackType == '{}'".format(healthTrackType[i].lower())
            if((i+1) < len(healthTrackType)):
                query_string += " or "
        query_string += ")"

        # Add to the SQL string if want to only check completed events.
        if(completed):
            query_string += " and (completed == 1)"

        filtered_entries = df.query(query_string)
        filtered_entries = filtered_entries[filtered_entries['healthTrackData'].notna()] #remove entries where the healthTrackData has no value. 

        grouping1 = filtered_entries.groupby('participantId')[sum].sum() # groups by participantID whilst summing the healthTrackingData values.
        return grouping1

    # Last Edit on 12/7/2022 by Reagan Kelley
    # Originally written from EMMA_data_wrangling.ipynb
    def create_variable(self, participants_dict, df, dataset_type, variable_name, variable_func, elementIDs = None, day_of_week=-1, distinct=False, tokens=None,
    sum = None, healthTrackType=None, completed=False, defined_variable_x = None):
        """ Creates a new variable and calculates it, storing the results for each participant in a dictionary.

        Args:
            participants_dict (Dict): Participant data, key = participantID, value = dict of variables
            df (DataFrame): An already created DataFrame that is data collected from some excel file
            dataset_type (Dataset.Type) : The type of data that is represented in df.
            variable_name (string): Identifier by which this variable is known as.
            elementIDs (list): A list of elementIDs that are counted and summed for this variable.
            variable_func (Lambda Function): Describes how the aggregated count will be calculated, typically division due to weekly or daily averages.
            day_of_week (int, optional): Allows us to filter the dataset further to only look at interactions on a specific day of the week (0 = Sunday to 6 = Saturday). Defaults to -1.
            distinct (bool, optional): Allows us to filter the dataset further to only count distinct uses (5 minute intervals). Defaults to False.
            tokens (list, optional): A string list of token names that each entry must also have. Defaults to [].

        Returns:
             Dict: An updated dictionary containing the calculated variable for all participants in the dataset, interactions_df
        """
        
        # Each is a pair (participantID, count)
        if(dataset_type == DatasetType.INTERACTIONS):
            element_count_list = self.get_interaction_counts(df, elementIDs, day_of_week=day_of_week, distinct=distinct, tokens=tokens).iteritems()
        elif(dataset_type == DatasetType.EVENTS):
            element_count_list = self.get_events_counts(df, sum, healthTrackType, completed=completed, day_of_week=day_of_week).iteritems()

        if(dataset_type == None):
            if(defined_variable_x is not None):
                for participant_id, variables in participants_dict.items():
                    X = variables.get(defined_variable_x) # get existing value for a variable

                    if(X is not None):
                        participants_dict[participant_id][variable_name] = eval(variable_func[1], {variable_func[0] : X}) # set variable x to an already defined variable
            else:
                raise Exception("No dataset given but also no defined variables given either.")
        else:
            for element_count in element_count_list:
                participant_id = element_count[0]
                if participant_id in participants_dict:
                    participants_dict[participant_id][variable_name] = eval(variable_func[1], {variable_func[0] : element_count[1]}) # eval example ("x", {"x" : count})
                else:
                    participants_dict[participant_id] = dict()
                    participants_dict[participant_id][variable_name] = eval(variable_func[1], {variable_func[0] : element_count[1]}) # eval example ("x", {"x" : count})
        
        return participants_dict
    
    # Last Edit on 12/7/2022 by Reagan Kelley
    # Originally written from EMMA_data_wrangling.ipynb
    def get_variable_calculations(self, interactions_df, events_df):
        """Given a week's worth of data in two DataFrames, interactions and events respectively, created a calculation table.

        Args:
            interactions_df (DataFrame): Contains interaction entries for a given week
            events_df (DataFrame): Contains event entries for a given week

        Returns:
            dict: [participant_id : the variable calculations for that participant]
        """
        participants = {}
        # * ================================================================
        # * Calculate variables for this week
        # * ================================================================
        for name, properties in self.variables.items(): # variable properties were gather from variable_definitions.json
            dataset_type = properties.dataset_type
            function = properties.lambda_function
            day_of_week = properties.day_of_week
            defined_variable_x = properties.defined_variable_x
            
            if(dataset_type == DatasetType.INTERACTIONS):
                elementIDs = properties.elementIDs
                tokens = properties.tokens
                distinct = properties.distinct
                participants = self.create_variable(
                    participants,                           # this participants dict will be updated
                    interactions_df,                        # the dataset used in this variable
                    dataset_type,                           # what type of dataset this variable needs
                    name,                                   # the name of the variable
                    function,                               # the lambda function to do on every aggregate call
                    elementIDs = elementIDs,                # elementIDs used
                    day_of_week=day_of_week,                # if not -1, specifies the day to calculate
                    distinct=distinct,                      # only count distinct uses
                    tokens=tokens,                          # what tokens to look at for the variable
                    defined_variable_x= defined_variable_x  # when not None, provided a definition for X for the function
                    )

            elif(dataset_type == DatasetType.EVENTS):
                sum = properties.sum
                healthTrackType = properties.healthTrackType
                completed = properties.completed
                participants = self.create_variable(
                    participants,                           # this participants dict will be updated
                    events_df,                              # the dataset used in this variable
                    dataset_type,                           # what type of dataset this variable needs
                    name,                                   # the name of the variable
                    function,                               # the lambda function to do on every aggregate call
                    day_of_week=day_of_week,                # if not -1, specifies the day to calculate
                    sum=sum,                                # the column to count
                    healthTrackType=healthTrackType,        # What tags to filter by for the healthTrackType
                    completed=completed,                    # only look at completed events when true
                    defined_variable_x= defined_variable_x  # when not None, provided a definition for X for the function
                )
            else:
                participants = self.create_variable(
                    participants,                           # this participants dict will be updated
                    None,                                   # the dataset used in this variable, when None used other defined variables
                    None,                                   # what type of dataset this variable needs
                    name,                                   # the name of the variable
                    function,                               # the lambda function, in this case includes predefined variables
                    day_of_week=day_of_week,                # if not -1, specifies the day to calculate
                    defined_variable_x=defined_variable_x   # when not None, provided a definition for X for the function.
                )

        # set the values of variables not calculated to 0 (the use of them by the participants never appeared in the dataset)
        for participant_id in participants:
            keys = participants[participant_id].keys()
            undeclared_variables = list(set(self.variableNames).difference(keys)) # these are the variables for each participant that were not calculated. (=0)
            for variable in undeclared_variables:
                participants[participant_id][variable] = 0
        
        return participants

        
    # Last Edit on 12/13/2022 by Reagan Kelley
    # Refactored to allow for event datasets
    def read_data(self):
        """Given a csv file, converts a dataset of interactions spanning many weeks into many datasets by week.

        Args:
            interactions_filename (string): Absolute filepath of excel file.

        Returns:
            Dict: Dictionary of interaction DataFrames. Key = StartDate, Value=DataFrame
        """
        # * ====================================================================
        # * Get interactions data
        # * ====================================================================
        if self.debug:
            print(colored("\nReading Interactions from Dataset...", 'blue'))

        if self.data[DatasetType.INTERACTIONS] == None:
            raise Exception("Interactions infile is None")

        # Get weekly dfs for interactions
        self.data[DatasetType.INTERACTIONS].read_file()

        if self.debug:
            print("* Results: {} weeks of data gathered.".format(len(self.data[DatasetType.INTERACTIONS].weekly_dfs)))

        # * ====================================================================
        # * Get events data
        # * ====================================================================
        if self.debug:
            print(colored("\nReading Events from Dataset...", 'blue'))

        if self.data[DatasetType.EVENTS] == None:
            raise Exception("Events infile is None")

        # Get weekly dfs for interactions
        self.data[DatasetType.EVENTS].read_file()

        if self.debug:
            print("* Results: {} weeks of data gathered.".format(len(self.data[DatasetType.EVENTS].weekly_dfs)))


    # Last Edit on 12/13/2022 by Reagan Kelley
    # Refactored to allow for event datasets
    def create_weekly_calculations_table(self, create_csvs=False, return_tables=False):
        """Given a large dataset of interactions from multiple participants, outputs all weekly csv files from that data showcasing desired calculated variables.

        Args:
            interactions_filename (string): Absolute path to large dataset
        """
        ret = []
        used_weeks = []
        extract_count = 0

        if self.debug:
            print(colored("\nCalculating Variables for each week...", 'blue'))
        

        for date, interactions_df in self.data[DatasetType.INTERACTIONS].weekly_dfs.items():
            filename = "Week {}, {}".format(date[0], date[1])  # The Week and Year of the next dataframe that will be used to calculate variables.
            events_df = self.data[DatasetType.EVENTS].weekly_dfs.get((date[0], date[1]))
            
            if(events_df is not None):
                used_weeks.append(date)
                if(self.debug):
                    print(f"* Calculating variables for ({filename})")
            
                participants = self.get_variable_calculations(interactions_df, events_df)  # Get variable calculations for each participant that week

                if(create_csvs):
                    self.participant_dict_to_csv(participants, "{}.csv".format(filename))      # Output results to the output directory
                
                if(return_tables):
                    ret.append(((date[0], date[1]), self.participant_dict_to_df(participants)))

                extract_count += 1
            else:
                pass

        if self.debug:
            unused = []
            for date in self.data[DatasetType.INTERACTIONS].weekly_dfs.keys():
                if(date not in used_weeks):
                    unused.append(["Interactions", date])
            for date in self.data[DatasetType.EVENTS].weekly_dfs.keys():
                if(date not in used_weeks):
                    unused.append(["Events", date])
            if(len(unused) > 0):
                print(colored("\n* Weeks not used ===========================", 'red'))
                print(pd.DataFrame(unused, columns=['Dataset', '(Week, Year)']))
                print(colored("============================================", 'red'))
        
        if self.debug:
            print(colored("\nOutput Results...", 'blue'))

            if(create_csvs):
                print("* {} calculation tables created in dir [{}]".format(extract_count, self.OUTPUT_DIR))
            if(return_tables):
                print("* {} calculation tables returned".format(extract_count))

        if(return_tables):
            return ret
        else:
            return None



# Last Edit on 12/7/2022 by Reagan Kelley
# Initial Implementation
def main():
    """Executes data wrangling from the provided command-line arguments
    """
    dw = DataWrangling(args = sys.argv[1:])   # use arguments to choose data files and user options (e.g. --debug)
    dw.read_data()                            # read data files provided in command line arguments
    dw.create_weekly_calculations_table(create_csvs=True)     # now that data file is read into program, output the variable calculations for each week.

if os.name == 'nt':
    just_fix_windows_console()

if __name__ == "__main__":
    main()