from src.participant import *

def main():
    # Get a dictionary of participants from interaction data
    participants = get_participants_from_interactions('data/Interactions 01_26_2022 after 10_31_2021.xlsx')

    val = ""
    while(val != '-1'):
        val = input("Enter ParticipantID for their interaction count: ")
        if int(val) in participants:
            print(participants[int(val)].get_interactions())
            print("\n")
        elif val != '-1':
            print("ParticipantID not found.")
    
    save_participants_to_file(participants, Append=False)

    # print("Participant's who did interaction: elementID = 3:")
    # for participant in participants:
    #     count = participants[participant].get_interaction_count(3)
    #     if(count > 0):
    #         print("participantID: {}, count: {}".format(participants[participant].get_participant_id(), count))



if __name__ == "__main__":
    main()