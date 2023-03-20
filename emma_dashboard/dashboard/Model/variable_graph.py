import pandas as pd

class VariableGraph:
    
    def __init__(self, title="Graph Title", graph_type="line", df = pd.DataFrame(), df_columns=[], scope='weekly', labels=[], border_color=[]):
        
        self.title = title
        self.type = str.lower(graph_type)
        self.scope = str.lower(scope)

        self.datasets = []
        if self.scope == 'weekly':
            for index, column in enumerate(df_columns):
                dataset = {}
                dataset['data'] = list(df[column])
                dataset['label'] = labels[index]
                dataset['border_color'] = border_color[index]

                print(dataset['data'])
                self.datasets.append(dataset)
            self.x_labels = ["Week {}, {}".format(row[0], row[1]) for row in df[['week_number', 'year_number']].values.tolist()]
            
            print("----------------------")

