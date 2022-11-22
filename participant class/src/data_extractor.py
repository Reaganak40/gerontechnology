import pandas as pd
import numpy as np
import os

# =================================================================
# Function: count_participant_interactions()
# Details: Using pandas, return a series that sums interactions 
#          of participants 
# Returns: Series
# =================================================================
def count_participant_interactions(interactions_filename):
    df = pd.read_excel(interactions_filename)
    return df.groupby(['participantId', 'elementId']).size()
    
