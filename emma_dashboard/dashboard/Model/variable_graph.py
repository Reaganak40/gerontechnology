#!/usr/bin/python

""" This file defines the VariableGraph class
"""

# * Modules
import pandas as pd


class VariableGraph:
    """ The VariableGraph class is really a helper class, with the use of jinja2, to define a chart.js graph in JavaScript.
    """
    def __init__(self, chart_id='NoID', title="Graph Title", graph_type="line", df = pd.DataFrame(), df_columns=[], scope='weekly', labels=[], border_color=[]):
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
        if self.scope == 'weekly':
            for index, column in enumerate(df_columns):
                dataset = {}
                dataset['data'] = list(df[column])
                dataset['label'] = labels[index]
                dataset['border_color'] = border_color[index]
                self.datasets.append(dataset)
            self.x_labels = ["Week {}, {}".format(row[0], row[1]) for row in df[['week_number', 'year_number']].values.tolist()]
            

