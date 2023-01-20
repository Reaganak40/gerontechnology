#!/usr/bin/python

""" This contains the Utils class which is used by other scripts in the 
    program for functional tasks that aren't use-cases.
"""

# * Modules
from datetime import datetime, timedelta
import pandas as pd

class Utils:
    # Last Edit on 12/7/2022 by Reagan Kelley
    # Originally written from EMMA_data_wrangling.ipynb
    def next_sunday(original_datetime : datetime) -> datetime:
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

    # Last Edit on 1/19/2023 by Reagan Kelley
    # Changed definition of distinct (in code)
    def filter_to_distinct_interactions(df : pd.DataFrame, sec_gap=300) -> pd.DataFrame:
        """Filters a dataframe to only include entries that are distinct use, that is the last action of a particular elementID happened more than sec_gap seconds ago.

        Args:
            df (DataFrame): The dataframe that will be filtered, should be limited to a day worth of entries.
            sec_gap (int, optional): The amount of seconds required for a distinct use. Defaults to 300.

        Returns:
            _type_: _description_
        """
        df = df.sort_values(by=['timestamp_local'])

        participant_distinct_use = {}
        not_distinct = []

        for index in range(len(df)):
            current_entry = df.iloc[index]

            # get participant for this row
            last_time = participant_distinct_use.get(current_entry['participantId'])
            
            if(last_time != None): # last_time is not None when there was a previous entry from this participant
                delta = current_entry['timestamp_local'] - last_time
                if(delta.total_seconds() < sec_gap):
                    not_distinct.append(index)
            
            # update participant's last used time to this entries time
            participant_distinct_use[current_entry['participantId']] = current_entry['timestamp_local']

        return df.drop(df.index[not_distinct])

    # Last Edit on 12/7/2022 by Reagan Kelley
    # Originally written from EMMA_data_wrangling.ipynb
    def filter_to_day_of_week(df : pd.DataFrame, day=0) -> pd.DataFrame:
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