#!/usr/bin/python

""" This file defines the VariableGraph class
"""

# * Modules
import pandas as pd

from datetime import date
import time

class VariableGraph:
    """ The VariableGraph class is really a helper class, with the use of jinja2, to define a chart.js graph in JavaScript.
    """
    def __init__(self, chart_id='NoID', title="Graph Title", graph_type="line", df = pd.DataFrame(), df_columns=[], scope='weekly',
                labels=[], border_color=[], num_charts = -1, pie_max = -1, progress_max=0, goal_line = None):
        """ Constructor for a VariableGraph object

        Args:
            chart_id (str, optional): This will be the chart variable name defined in JavaScript. Defaults to 'NoID'.
            title (str, optional): The title of the graph, to show on top of graph. Defaults to "Graph Title".
            graph_type (str, optional): What kind of graph to create. Defaults to "line".
            df (_type_, optional): The weekly calculation tables for a single participant. Defaults to pd.DataFrame().
            df_columns (list, optional): The columns in the calculation table that will be used for data-points. Defaults to [].
            scope (str, optional): Weekly or daily, determines if the x-axis is to show weekly or daily intervals. Defaults to 'weekly'.
            labels (list, optional): For each column which represents a variable, the label is the name of that variable. Defaults to [].
            border_color (list, optional): For each column which represents a variable, choose a color which will be used in the graph for its data-points. Defaults to [].
        """
        self.title = title
        self.type = str.lower(graph_type)
        self.scope = str.lower(scope)
        self.id = chart_id

        # for each variable to be represented in the graph, construct a chart.js dataset.
        self.datasets = []

        self.progress_max = progress_max

        # Determine how recent in weeks to get charts for.
        if num_charts < 0:
            slice_size = len(df)
        else:
            slice_size = min(len(df), num_charts)
        
        df = df[-slice_size:]  
        self.num_charts = slice_size

        # * ==================================
        # *      -- CREATE PIE CHART --
        # * ==================================
        if self.type == 'pie':
            

            if self.scope != 'weekly':
                raise Exception("Daily scope for pie chart not possible.")

            for row_index in range(len(df)):
                dataset = {}
                dataset['title'] = "{}: Week {}, {}".format(self.title, int(df.iloc[row_index][0]), int(df.iloc[row_index][1]))
                
                dataset['data'] = []
                for index, column in enumerate(df_columns):
                        dataset['data'].append(df.iloc[row_index][column])
                
                dataset['labels'] = labels[:]
                dataset['border_color'] = border_color[:]
                if pie_max >= 0:
                    total = sum(dataset['data'])
                    left_over = max(pie_max - total, 0)
                    
                    if left_over > 0:
                        dataset['labels'].append('left_over')
                        dataset['data'].append(left_over)
                        dataset['border_color'].append('white')

                self.datasets.append(dataset)
        
        # * ==================================
        # *    -- CREATE PROGRESS CHART --
        # * ==================================
        elif self.type == 'progress':

            last_index = len(df) - 1
            for row_index in range(len(df)):
                dataset = {}
                dataset['title'] = "{}: Week {}, {}".format(self.title, int(df.iloc[row_index][0]), int(df.iloc[row_index][1]))

                if row_index == last_index:
                    dataset['title'] += ' (Latest)'
                
                
                dataset['data'] = []
                for index, column in enumerate(df_columns):
                        dataset['data'].append(round(df.iloc[row_index][column], 2))
                
                dataset['labels'] = labels[:]
                dataset['border_color'] = border_color[:]

                self.datasets.append(dataset)
        
        # * =====================================
        # *    -- CREATE LINE OR BAR CHART --
        # * =====================================
        else:
                    
            if self.scope == 'weekly':
                for index, column in enumerate(df_columns):
                    dataset = {}
                    dataset['data'] = list(df[column])
                    dataset['label'] = labels[index]
                    dataset['border_color'] = border_color[index]
                    self.datasets.append(dataset)
                self.x_labels = ["Week {}, {}".format(row[0], row[1]) for row in df[['week_number', 'year_number']].values.tolist()]
            
            else:
                try:
                    #scope is daily
                    
                    self.x_labels = []
                    count = 0
                    for index, daily_var in enumerate(df_columns):
                        dataset = {}
                        dataset['data'] = []
                        dataset['label'] = labels[index]
                        dataset['border_color'] = border_color[index]

                        # create sql column names for daily variable
                        daily_columns = [daily_var + '_' + day + 'day' for day in ['Mon', 'Tues', 'Wednes', 'Thurs', 'Fri', 'Satur', 'Sun']]

                        # append all daily entries in chronological order
                        for row_index in range(len(df)):
                            for column in daily_columns:
                                dataset['data'].append(df.iloc[row_index][column])
                            
                        
                            week, year = df.iloc[row_index][['week_number', 'year_number']]
                            
                            for day in range(1, 8):
                                calender_date = date.fromisocalendar(int(year), int(week), day)
                                self.x_labels.append(str(calender_date) + " 00:00:00 GMT+0800")
                                print(f"{count}: ",str(calender_date) + " 00:00:00")
                                count += 1
                                #print(calender_date, daily_columns[day-1], dataset['data'][-(8-day)])
                        self.datasets.append(dataset)

                except Exception as e:
                    print(e)

            if goal_line is not None:
                if str.lower(goal_line[0]) == 'static':
                    self.goal_line = [goal_line[1]] * len(self.datasets[0]['data'])
            else:
                self.goal_line = None
                

