#!/usr/bin/python

""" Takes existing data analysis for EMMA and transforms it to a universal set that can be compared to newer calculations.
"""

# * Imports
import os
import pandas as pd

# ===========================================================================================================
# ? STRUCTURE OF FRANCIS CALCULATED VARIABLES - AFTER MANUALLY NORMALIZED
# ===========================================================================================================
TARGET_FILE = os.getcwd() + R"\..\tests\test data\output\BB_Adherence Data_Cohort 1_5.2 - NormalizedPre.xlsx"
START_OF_DAILY_VARIABLES = 73
START_DAY = 155
END_DAY = 182
FIRST_WEEK = 23
LAST_WEEK = 26
FIRST_PARTICIPANT = 95
# ===========================================================================================================

class VariableType():
    WEEKLY = 0
    DAILY = 1

def get_variable(df, participant=FIRST_PARTICIPANT, variable_name = "CalenderUse", variable_type = VariableType.WEEKLY, week=FIRST_WEEK, day_of_week=0):
    row = df.loc[df['participantId'] == participant]

    if(variable_type == VariableType.WEEKLY):
        relative_week = week - FIRST_WEEK
        if(relative_week > 0):
            variable_name += ".{}".format(relative_week)
        return row[variable_name].values[0]


def normalize():
    df = pd.read_excel(TARGET_FILE, skiprows=[0])

    val = get_variable(
        df,
        participant=131,
        variable_name= "CalendaringGoal", 
        variable_type=VariableType.WEEKLY,
        week = (26)
        )
    print(val)


if __name__ == "__main__":
    normalize()