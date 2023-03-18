from dashboard import db

class Participant:
    def __init__(self, id):
        _info = db.get_user(id)
        if(len(_info) == 0):
            raise KeyError("ID Not Found")
        info = _info.iloc[0]

        self.id = info['participant_id']
        self.name = info['participant_name']
        self.study = info['study']
        self.cohort = info['cohort']
        self.active = info['active']

        self.get_dates()
        self.get_tables()
    
    def get_tables(self):
        self.tables = db.get_tables(self.id).drop(columns=['participant_id'])
    
    def get_dates(self):
        pass
