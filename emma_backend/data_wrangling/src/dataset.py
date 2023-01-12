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
    
    # Last Edit on 12/13/2022 by Reagan Kelley
    # Initial Implementation
    def IsType(val):
        """Returns true if a provided value is a defined enumerator for a DatasetType

        Args:
            val (int): Enumerator, int identifier for a dataset

        Returns:
            Bool: True if this int enum is defined, false otherwise.
        """
        return True if val == DatasetType.INTERACTIONS or val == DatasetType.EVENTS else False

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
            self.infile = infile        # The filepath to the read file

            if not self.infile.exists():
                raise FileNotFoundError(colored("[Data Wrangling Error]\nThe provided file does not exist:\n{}".format(self.infile), "yellow"))

            self.weekly_dfs : dict[tuple, pd.DataFrame] = {}        # This will eventually contain parsed datasets from the original dataset, but separated by weekly segments.

        # Last Edit on 12/13/2022 by Reagan Kelley
        # Initial Implementation
        def read_file(self):
            """ Reads the provided infile and takes that dataset and parses it into weekly segments. Results are in weekly_dfs.
            """
            
            # * Read Interactions Excel File and transform to weekly dataframes (weekly_dfs)
            if self.type == DatasetType.INTERACTIONS:
                # gets the entire dataset from the provided infile.
                interactions_raw = pd.read_excel(self.infile)

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

            # * Read Events Excel File and transform to weekly dataframes (weekly_dfs)
            elif self.type == DatasetType.EVENTS:
                # gets the entire dataset from the provided infile.
                events_raw = pd.read_excel(self.infile)
                
                # Get the date range in the dataset -> will be used to create weekly dataframes
                start_date = events_raw['timestamp_local'].min()  # the earliest entry in the dataset
                end_parsec = Utils.next_sunday(start_date)              # the beginning of the next week
                end_date = events_raw['timestamp_local'].max()    # the latest entry in the dataset

                # separate entries by weekly ranges (sunday to saturday)
                while(start_date < end_date):
                    df = events_raw.loc[(events_raw["timestamp_local"] >= start_date) & (events_raw["timestamp_local"] < end_parsec)]
                    self.weekly_dfs[(start_date.strftime("%U"), start_date.strftime("%Y"))] = df        
                    start_date = end_parsec
                    end_parsec = Utils.next_sunday(start_date)