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
        self.elementIDs = variable_definition["elementIDs"]
        self.lambda_function = variable_definition["function"]

        if variable_definition["dataset"] == "Interactions":
            self.dataset_type = DatasetType.INTERACTIONS
        elif variable_definition["dataset"] == "Events":
            self.dataset_type = DatasetType.EVENTS
        else:
            raise Exception("Variable {} does not have properly defined dataset type: {}".format(self.name, variable_definition["dataset"]))

        self.tokens = variable_definition.get("tokens", None)
        self.distinct = variable_definition.get("distinct", False)
        self.day_of_week = day_of_week

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
    if(variable_definition["scope"] == "daily"): 
        day_of_week = 0
        for day in ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]:
            variable_definition["name"] = name + "-{}".format(day)
            res.append(Variable(variable_definition, day_of_week))
            day_of_week += 1
    elif (variable_definition["scope"] == "weekly"):
        res.append(Variable(variable_definition, -1))
    else:
        raise Exception("Variable Scope '{}' is not a defined range".format(variable_definition["scope"]))

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