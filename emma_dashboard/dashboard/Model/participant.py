from dashboard import db
from .variable_graph import VariableGraph

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

        self.get_tables()
        self.get_graphs()
    
    def get_tables(self):
        self.tables = db.get_tables(self.id).drop(columns=['participant_id']).sort_values(by=['year_number', 'week_number'], axis=0)
    
    def get_graphs(self):
        self.graphs : dict[VariableGraph] = {}
        self.graphs['PE'] = VariableGraph(
            title         = "Physical Exercise",
            graph_type    = "line",
            df            = self.tables, 
            df_columns    = ['v_TotalPEWeeklyPHEX'], 
            scope         = 'weekly', 
            labels        = ['Weekly Hours of Activity'],
            border_color  = ['red']
            )
