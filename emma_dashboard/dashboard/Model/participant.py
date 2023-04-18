#!/usr/bin/python

""" This file defines the Participant class
"""

# * Modules
# Local Imports
from dashboard import db
from .variable_graph import VariableGraph

# * Quick Reference =============================================================================
# * Participant     => Participant wrapper class that is used to contain all dashboard info for that participant.
# * get_tables      => Gets or updates the weekly calculation tables that contain this participants EMMA variables.
# * get_graphs      => Gets or updates the graphs for the EMMA calculation variables
# * =============================================================================================

class Participant:
    """ Contains all use data about a participant so jinja2 may access it, specifically for the participant route.
    """
    def __init__(self, id):
        """Constructor for Participant object

        Args:
            id (int): The unique ID of this participant, which is used to access 
            the database and find the rest of the information about the participant

        Raises:
            KeyError: Raises when the participant_id does not match any user in the database.
        """
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
        """ Gets the calculation tables from the database for this participant, and makes sure it is in chronological order.
        """
        self.tables = db.get_tables(self.id).drop(columns=['participant_id']).sort_values(by=['year_number', 'week_number'], axis=0)
    
    def get_graphs(self):
        """ After getting the calculation tables, uses the VariableGraph class to create a dictionary of
            graphs that will by chart.js when accessing the participant page.
        """
        self.graphs : dict[VariableGraph] = {}
        
        # * GRAPH DEFINITIONS
        
        # ==========================================
        # Snapshot Data
        # ==========================================
        self.graphs['totalCalenderInteractions'] = VariableGraph(
            chart_id      = 'TCI_chart',
            title         = "Total Calender Interactions",
            graph_type    = "line",
            df            = self.tables, 
            df_columns    = ['v_SumTotalCalendarInteractions'], 
            scope         = 'weekly', 
            labels        = ['Daily Average Activity'],
            border_color  = ['#0000FF'],
            )
        
        self.graphs['totalEventInteractions'] = VariableGraph(
            chart_id      = 'TEI_chart',
            title         = "Total Event Interactions",
            graph_type    = "line",
            df            = self.tables, 
            df_columns    = ['v_SumTotalEventInteractions'], 
            scope         = 'weekly', 
            labels        = ['Daily Average Activity'],
            border_color  = ['#0000FF'],
            )

        # ==========================================
        # Health Tracking Data
        # ==========================================
        self.graphs['PE'] = VariableGraph(
            chart_id      = 'PE_chart',
            title         = "Physical Exercise",
            graph_type    = "line",
            df            = self.tables, 
            df_columns    = ['v_TotalPEWeeklyPHEX'], 
            scope         = 'weekly', 
            labels        = ['Weekly Activity'],
            border_color  = ['#0000FF'],
            goal_line     = ('static', 150)
            )

        self.graphs['CE'] = VariableGraph(
            chart_id      = 'CE_chart',
            title         = "Cognitive Exercise",
            graph_type    = "line",
            df            = self.tables, 
            df_columns    = ['v_TotalCEWeeklyMEEX'], 
            scope         = 'weekly', 
            labels        = ['Weekly Activity'],
            border_color  = ['#A52A2A'],
            goal_line     = ('static', 12)
            )
        
        self.graphs['WE'] = VariableGraph(
            chart_id      = 'WE_chart',
            title         = "Well-being Exercise",
            graph_type    = "line",
            df            = self.tables, 
            df_columns    = ['v_TotalWEWeeklyWELLX'], 
            scope         = 'weekly', 
            labels        = ['Weekly Activity'],
            border_color  = ['#228B22'],
            goal_line     = ('static', 3)
            )
        
        self.graphs['h_goals'] = VariableGraph(
            chart_id       = 'h_goals_chart',
            title          = "Health Goals",
            graph_type     = "progress",
            df             = self.tables, 
            df_columns     = ['v_PEGoal', 'v_CEGoal', 'v_WEGoal'], 
            scope          = 'weekly', 
            labels         = ['PE Goal', 'CE Goal', 'WE Goal'],
            border_color   = ['#00FFFF', '#C19A6B', '#AFE1AF'],
            num_charts = 4,
            progress_max=1,
            )
        
        # ==========================================
        # General Use Data
        # ==========================================
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
