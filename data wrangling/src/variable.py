#!/usr/bin/python

# * Modules
import json
from dataset import DatasetType
from typing import Callable

class Variable:

    def __init__(self, variable_func : Callable, variable_definition : dict):
        self.variable_func = variable_func

        self.name = variable_definition["name"]
        self.elementIDs = variable_definition["elementIDs"]
        self.lambda_function = variable_definition["function"]

        self.tokens = variable_definition.get("tokens", None)
        self.distinct = variable_definition.get("distinct", False)

    def evaluate(self, participants, df,):
        return self.variable_func(df)


def variable_factory(variable_definition : dict, variable_func_dict : dict[int, Callable]):
    res = []

    name = variable_definition["name"]
    dataset_type = None
    
    # check that the provided dataset option is a defined one
    if(variable_definition["dataset"] == "Interactions"):
        dataset_type = DatasetType.INTERACTIONS
    elif (variable_definition["dataset"] == "Events"):
        dataset_type = DatasetType.EVENTS
    else:
        raise Exception("Variable Definition uses unknown dataset type: {}".format(variable_definition["dataset"]))
    
    variable_func = variable_func_dict[dataset_type]
    
    # if daily, provide 7 variables with the day in their definition name.
    if(variable_definition["scope"] == "daily"): 
        for day in ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]:
            variable_definition["name"] = name + "-{}".format(day)
            res.append(Variable(variable_func, variable_definition))
    elif (variable_definition["scope"] == "weekly"):
        res.append(Variable(variable_func, variable_definition))
    else:
        raise Exception("Variable Scope '{}' is not a defined range".format(variable_definition["scope"]))



def create_variable_dictionary(filename, variable_func_dict : dict[int, Callable]):
    variables = {}
    with open(filename) as json_file:
        data = json.load(json_file)
        variable_defs = data['Variables']

        for vd in variable_defs:
            variable_s = variable_factory(vd, variable_func_dict)
    
    return variables

def f1():
    pass

if __name__ == "__main__":
    create_variable_dictionary("variable_definitions.json", {DatasetType.INTERACTIONS : f1, DatasetType.EVENTS : f1})