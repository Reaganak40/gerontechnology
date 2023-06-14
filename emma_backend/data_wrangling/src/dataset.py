#!/usr/bin/python

""" Contains the class instances that model provided datasets for the EMMA app (interactions and events)
"""
# * Modules
import pandas as pd
from pathlib import Path
from colorama import just_fix_windows_console
from termcolor import colored

# Local Imports
from utils import Utils

class DatasetType():
    INTERACTIONS = 0
    EVENTS = 1
    ENTRIES = 2
    
    # Last Edit on 12/13/2022 by Reagan Kelley
    # Initial Implementation
    def IsType(val):
        """Returns true if a provided value is a defined enumerator for a DatasetType

        Args:
            val (int): Enumerator, int identifier for a dataset

        Returns:
            Bool: True if this int enum is defined, false otherwise.
        """
        return True if val == DatasetType.INTERACTIONS or val == DatasetType.EVENTS or val == DatasetType.ENTRIES else False
    
    def NameOfType(val):
        if val == DatasetType.INTERACTIONS:
            return "Interactions"
        if val == DatasetType.EVENTS:
            return "Events"
        if val == DatasetType.ENTRIES:
            return "Entries"
        return None

class Dataset:
        # Last Edit on 12/13/2022 by Reagan Kelley
        # Initial Implementation
        def __init__(self, dataset_type : int, infile : Path):
            """ Creates a new instance of a dataset, which included the utility functions to manage and parse the dataset.

            Args:
                dataset_type (Enum of DatasetType): Identifies the type of dataset this is.
                infile (string): The filepath to where the dataset file. EXCEL FILE

            Raises:
                Exception: Throws if the dataset_type is not defined.
            """
            if DatasetType.IsType(dataset_type) == False:
                raise Exception("Invalid dataset_type argument. {}".format(dataset_type))
            
            self.type = dataset_type    # the type of data in this Dataset -> Events or interactions
            self.name = DatasetType.NameOfType(self.type)
            self.infile = infile        # The filepath to the read file

            if not self.infile.exists():
                raise FileNotFoundError(colored("[Data Wrangling Error]\nThe provided file does not exist:\n{}".format(self.infile), "yellow"))

            self.weekly_dfs : dict[tuple, pd.DataFrame] = {}        # This will eventually contain parsed datasets from the original dataset, but separated by weekly segments.

        def read_file(self):
            """ Reads the provided infile and takes that dataset and parses it into weekly segments. Results are in weekly_dfs.
            """
            
            # gets the entire dataset from the provided infile.
            raw_df = pd.read_excel(self.infile)
            lc_columns = [str.lower(x) for x in raw_df.columns]
            
            # * ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            # * Validate columns according to the dataset type
            # * ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            if self.type == DatasetType.INTERACTIONS:
                needed_columns = ['interactionid','participantid','elementid','timestamp_local','interaction','token','type','source']

            elif self.type == DatasetType.EVENTS:
                needed_columns = ['eventid', 'participantid', 'eventtoken', 'action', 'timestamp_local', 'timestamp_utcoffset', 'eventtype', 
                                  'eventdate', 'nospecifiedtime', 'starttime', 'endtime', 'priority', 'reminderprior', 'reminderpriorsixth',
                                  'reminderpriorquarter', 'reminderpriorhalf', 'reminderpriorwhole', 'reminderatevent', 'completed', 'recurring',
                                  'recurringstartdate', 'recurringenddate', 'recurringfrequency', 'recurringsunday', 'recurringmonday',
                                  'recurringtuesday', 'recurringwednesday', 'recurringthursday', 'recurringfriday', 'recurringsaturday',
                                  'recurringhide', 'ishealthtrack', 'healthtrackgoal', 'healthtrackdata', 'healthtracktype']
            
            elif self.type == DatasetType.ENTRIES:
                needed_columns = ['entryid', 'participantid', 'timestamp_local', 'timestamp_utcoffset', 'entrytoken', 'entrytype', 'action',
                                  'title', 'content', 'imagesaved', 'folderentryid', 'frequency', 'templateid', 'foldersetid', 'isstatic', 'foldertoken']
            
            for nd in needed_columns:
                if nd not in lc_columns:
                    err_msg = colored(f"[Data Wrangling Error]\nThe provided {self.name} file does not contain the required '{nd}' column.", 'red')
                    raise Exception(err_msg)
            
            # * ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            # * Read excel file and transform to 
            # * weekly dataframes (weekly_dfs)
            # * ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            
            # Get the date range in the dataset -> will be used to create weekly dataframes
            start_date = raw_df['timestamp_local'].min()  # the earliest entry in the dataset
            end_parsec = Utils.next_sunday(start_date)              # the beginning of the next week
            end_date = raw_df['timestamp_local'].max()    # the latest entry in the dataset

            # separate entries by weekly ranges (sunday to saturday)
            while(start_date < end_date):
                df_in_weekly_range = raw_df.loc[(raw_df["timestamp_local"] >= start_date) & (raw_df["timestamp_local"] < end_parsec)]
                self.weekly_dfs[(start_date.strftime("%U"), start_date.strftime("%Y"))] = df_in_weekly_range        
                start_date = end_parsec
                end_parsec = Utils.next_sunday(start_date)
                

