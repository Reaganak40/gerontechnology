#!/usr/bin/python

""" This contains the Utils class which is used by other scripts in the 
    program for functional tasks that aren't use-cases.
"""

# * Modules
from datetime import datetime, timedelta, date
import pandas as pd
from termcolor import colored

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
            sec_gap (int, optional): The amount of seconds required for a distinct use. Defaults to 300 (5 minutes).

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

    def df_filter_by(df, filter_by):
        # create a SQL string to filter DataFrame to only include rows with filter values
        query_string = ""
        index = 0
        for column_name, filter_value in filter_by:
            if type(filter_value) is int or type(filter_value) is bool:
                query_string += '({} == {})'.format(column_name, filter_value)
            elif type(filter_value) is str:
                query_string += '({} == "{}")'.format(column_name, filter_value.lower())
            elif type(filter_value) is list:
                if len(filter_value) > 0:
                    query_string += "("
                    for i in range(len(filter_value)):
                        if type(filter_value[i]) is int:
                            query_string += '{} == {}'.format(column_name, filter_value[i])
                        elif type(filter_value[i]) is str:
                            query_string += '{} == "{}"'.format(column_name, filter_value[i])
                        else:
                            raise Exception("Unsupported list element: {}".format(type(filter_value[i])))

                        if((i+1) < len(filter_value)):
                            query_string += " or "
                    query_string += ")"
                else:
                    raise Exception("filter_by variable of type 'list' cannot be empty")
            else:
                raise Exception("filter_by variable of type '{}' is not supported".format(type(filter_value)))

            index += 1
            if index < len(filter_by):
                query_string += " and "
        return df.query(query_string)
    
    def get_calculation_from_text(df, text_column, text_action):
        # only look at the columns to count text from (keep the participant ids)
        df = df[['participantId'] + text_column]
        
        # need to check if numeric type before dropping NaN values. Numeric columns will not provide accurate character counts.
        for column in text_column:
            if pd.api.types.is_numeric_dtype(df[column].dtype):
                err_msg = colored(f"EMMA Data-Wrangling Error: Column ['{column}'] is not a string dtype.", 'red')
                raise Exception(err_msg)
        
        df = df.fillna('')
        
        # perform the text action on the text columns
        if text_action == 'character_count':
            for column in text_column:
                df[column + '_count'] = df[column].astype(str).str.len()
        elif text_action == 'word_count':
            for column in text_column:
                df[column + '_count'] = df[column].astype(str).str.count(' ') + 1
        else:
            err_msg = colored(f"EMMA Data-Wrangling Error: Undefined text-action {text_action}", 'red')
            raise Exception(err_msg)
        
        df['joined_sum'] = df[[col_name + "_count" for col_name in text_column]].sum(axis=1)        
        return df.groupby('participantId')['joined_sum'].sum() # groups by participantID whilst summing the sum-column values
        
    def get_calculation_from_count(df, count):
        return df.groupby('participantId')[count].count() # groups by participantID whilst summing the count of value instances.
    
    def get_calculation_from_sum(df, sum):
        return df.groupby('participantId')[sum].sum() # groups by participantID whilst summing the sum-column values.