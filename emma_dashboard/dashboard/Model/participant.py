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
            chart_id      = 'PE_chart',
            title         = "Physical Exercise",
            graph_type    = "line",
            df            = self.tables, 
            df_columns    = ['v_TotalPEWeeklyPHEX', 'v_PEGoal'], 
            scope         = 'weekly', 
            labels        = ['Weekly Hours of Activity', 'PE Goal'],
            border_color  = ['#0000FF', '#00FFFF']
            )

        self.graphs['CE'] = VariableGraph(
            chart_id      = 'CE_chart',
            title         = "Cognitive Exercise",
            graph_type    = "line",
            df            = self.tables, 
            df_columns    = ['v_TotalCEWeeklyMEEX', 'v_CEGoal'], 
            scope         = 'weekly', 
            labels        = ['Weekly Hours of Activity', 'CE Goal'],
            border_color  = ['#A52A2A', '#C19A6B']
            )
        
        self.graphs['WE'] = VariableGraph(
            chart_id      = 'WE_chart',
            title         = "Well-being Exercise",
            graph_type    = "bar",
            df            = self.tables, 
            df_columns    = ['v_TotalWEWeeklyWELLX', 'v_WEGoal'], 
            scope         = 'weekly', 
            labels        = ['Weekly Hours of Activity', 'WE Goal'],
            border_color  = ['#228B22', '#AFE1AF']
            )
        
        self.graphs['SumTotalEvent'] = VariableGraph(
            chart_id      = 'SumTotalEvent_chart',
            title         = "Total Event Interactions",
            graph_type    = "line",
            df            = self.tables, 
            df_columns    = ['v_SumTotalEventInteractions'], 
            scope         = 'weekly', 
            labels        = ['Weekly Event Totals'],
            border_color  = ['#CF9FFF']
            )
