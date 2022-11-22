from .data_extractor import *

class Participant:

    # =================================================================
    # Function: Participant.__init__()
    # Details: Class Constructor, 
    #          interaction = pair(elementID, num_interactions)
    # Returns: Nothing
    # =================================================================
    def __init__(self, participant_id, interaction = None):
        self.participant_id = participant_id
        self.interactions = dict()
        if(interaction != None): 
            self.add_to_interactions(interaction[0], interaction[1])
        self.interactions_df = None

    # =================================================================
    # Function: Participant.get_participant_id()
    # Details: Returns the ID of Participant
    # Returns: Int
    # =================================================================
    def get_participant_id(self):
        return self.participant_id
    
    # =================================================================
    # Function: Participant.add_to_interactions()
    # Details: An element_id represents a specific interaction. Given 
    #          an element_id add num_interactions to the total 
    #          interactions for that interaction.
    # Returns: Nothing
    # =================================================================
    def add_to_interactions(self, element_id, num_interactions):
        if element_id in self.interactions:
            self.interactions[element_id] += num_interactions
        else:
            self.interactions[element_id] = num_interactions
    
    # =================================================================
    # Function: Participant.get_interaction_count()
    # Details: Returns the total amount of instances a participant 
    #          did a given interaction.
    # Returns: Int
    # =================================================================
    def get_interaction_count(self, element_id):
        if element_id in self.interactions:
            return self.interactions[element_id]
        else:
            return 0
    # =================================================================
    # Function: Participant.get_interactions()
    # Details: Returns a dataframe representation of interaction 
    #          sum data
    # Returns: Dataframe
    # =================================================================
    def get_interactions(self):
        if self.interactions_df == None:
            self.interactions_df = pd.DataFrame.from_dict(self.interactions, orient='index', columns=['count'])
            self.interactions_df.reset_index(inplace=True)
            self.interactions_df.rename({'index':'elementID'}, axis='columns', inplace=True)
        return self.interactions_df

    # =================================================================
    # Function: Participant.save_to_file()
    # Details: Saves this instance to a file (named after the 
    #          participantID), using dataframes and saving to csv
    # Returns: Nothing
    # =================================================================
    def save_to_file(self, directory_path):
        interactions_df = pd.DataFrame.from_dict(self.interactions, orient='index', columns=['count'])
        interactions_df.reset_index(inplace=True)
        interactions_df.rename({'index':'elementID'}, axis='columns', inplace=True)

        if not os.path.exists(directory_path):
            os.makedirs(directory_path)

        interactions_df.to_csv(directory_path + '/participantID_{}_interactions.csv'.format(self.get_participant_id()))
        
# =================================================================
# Function: get_participants_from_interactions()
# Details: Given an excel file which contains interaction data, 
#          extract that data and add the total of interaction 
#          instances in a class object that represents the 
#          participant. Return a dictionary of participants.
# Returns: Dict()
# =================================================================
def get_participants_from_interactions(interactions_filename):
    
    # get series: participantID -> elementID -> count
    s = count_participant_interactions(interactions_filename)

    # Each interaction is a pair ([participantID, elementID], count)
    interactions =  s.iteritems()
    
    # Add interactions to Participant (create instances)
    participants = dict()
    for i in interactions:
        # i[0][0] is participantID
        # i[0][1] is elementID
        # i[1]    is interaction count
        participant_id = i[0][0]

        if participant_id in participants:
            participants[participant_id].add_to_interactions(i[0][1], i[1])
        else:
            participants[participant_id] = Participant(participant_id, (i[0][1], i[1]))

    return participants

# =================================================================
# Function: save_participants_to_file()
# Details: Given a dictionary of participants, saves all instance 
#          data to the saved directory. If Append is True (default), 
#          then instance values will be appended to previously 
#          saved data.
# Returns: Nothing
# =================================================================
def save_participants_to_file(participants, Append=True):
    if(Append):
        pass # TODO: Implement Append data to existing csv(s)
    else:
        for p in participants:
            participants[p].save_to_file('./data/saved/' + str(p))

# =================================================================
# Function: get_participants()
# Details: Returns a dictionary of participants from the saved 
#          directory. Returns all participants (default), or a 
#          specified list or range.
# Returns: Dict()
# =================================================================
def get_participants(Participants = None):
    pass
