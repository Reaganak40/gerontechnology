from dashboard import db

class Participant:
    def __init__(self, id):
        _info = db.get_user(id)
        if(len(_info) == 0):
            raise Exception("ID Not Found")
        
        info = _info.iloc[0]

        self.id = info['participant_id']
        self.name = info['participant_name']
        self.study = info['study']
        self.cohort = info['cohort']
        self.active = info['active']

