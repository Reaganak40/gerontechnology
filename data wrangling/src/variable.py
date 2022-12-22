#!/usr/bin/python

""" Given a json file with definitions of variables, creates a
    dictionary for those variables to be used in data wrangling.
"""

# * Modules
import json
from dataset import DatasetType

# Last Edit on 12/16/2022 by Reagan Kelley
# Initial Implementation
class Variable:
    def __init__(self, variable_definition : dict, day_of_week):
        """Holds the definition of a variable through a dictionary of variable attributes

        Args:
            variable_definition (dict): Holds the variable definition attributes such as the name and the elementIDs used.
        """
        self.name = variable_definition["name"]
        self.lambda_function = variable_definition["function"]
        
        if variable_definition.get("dataset") == None:
            self.dataset_type = None
        elif variable_definition["dataset"] == "Interactions":
            self.dataset_type = DatasetType.INTERACTIONS
        elif variable_definition["dataset"] == "Events":
            self.dataset_type = DatasetType.EVENTS

        self.tokens = variable_definition.get("tokens", None)
        self.distinct = variable_definition.get("distinct", False)
        self.elementIDs = variable_definition.get("elementIDs", None)
        self.sum = variable_definition.get("sum", None)
        self.healthTrackType = variable_definition.get("healthTrackType", None)
        self.completed = variable_definition.get("completed", False)
        self.day_of_week = day_of_week

        self.defined_variable_x = variable_definition.get("defined-variable-x", None)
        # TODO: Add functionality for multiple predefined variables

# Last Edit on 12/16/2022 by Reagan Kelley
# Initial Implementation
def variable_factory(variable_definition : dict):
    """Creates and returns a list of variables. This may be a list of one if the definition is weekly or up to 7 if daily.

    Args:
        variable_definition (dict): Holds the variable definition attributes such as the name and the elementIDs used.

    Raises:
        Exception: Throws an exception if the scope is not properly defined.

    Returns:
        List[Variable]: Each element holds a unique variable definition.
    """
    res : list[Variable] = []

    name = variable_definition["name"]
    
    # if daily, provide 7 variables with the day in their definition name.
    if(variable_definition.get("scope") == "daily"): 
        day_of_week = 0
        for day in ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]:
            variable_definition["name"] = name + "-{}".format(day)
            res.append(Variable(variable_definition, day_of_week))
            day_of_week += 1
    else:
        # if not daily or not defined, assume weekly
        res.append(Variable(variable_definition, -1))

    return res

# Last Edit on 12/16/2022 by Reagan Kelley
# Initial Implementation
def create_variable_dictionary(filename):
    """Reads through a json file which contains variable definitions for EMMA calculations.

    Args:
        filename (string): This file must be in the same directory as the python scripts, otherwise its an absolute path

    Returns:
        Dict [string, Variable]: Returns all the variable definitions in the JSON file
    """

    variables = {}
    with open(filename) as json_file:
        data = json.load(json_file)
        variable_defs = data['Variables']

        for vd in variable_defs:
            variable_s = variable_factory(vd)
            for variable in variable_s:
                variables[variable.name] = variable
    return variables

if __name__ == "__main__":
    create_variable_dictionary("variable_definitions.json")