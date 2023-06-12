#!/usr/bin/python

""" Given a json file with definitions of variables, creates a
    dictionary for those variables to be used in data wrangling.
"""

# * Modules
import copy
import json
import os
from termcolor import colored
# Local Imports
from dataset import DatasetType

# Last Edit on 12/16/2022 by Reagan Kelley
# Initial Implementation
class Variable:
    def __init__(self, variable_definition : dict, day_of_week):
        """Holds the definition of a variable through a dictionary of variable attributes

        Args:
            variable_definition (dict): Holds the variable definition attributes such as the name and the elementIDs used.
        """
        
        # * ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # * Get universal attributes
        # * ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self.name = variable_definition["name"]
        try:
            self.lambda_function = variable_definition["function"]
        except:
            err_msg = colored(f'EMMA Data-Wrangling Error: Variable definition [{self.name}] missing function attribute.', "red")
            raise NameError(err_msg)
        self.day_of_week = day_of_week
        
        self.study = variable_definition.get("study", None)
        
        if variable_definition.get("dataset") == None:
            self.dataset_type = None
        elif variable_definition["dataset"] == "Interactions":
            self.dataset_type = DatasetType.INTERACTIONS
        elif variable_definition["dataset"] == "Events":
            self.dataset_type = DatasetType.EVENTS

        
        # * ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # * Get interactions attributes if Interactions Variable
        # * Make none for attributes otherwise to avoid contamination
        # * ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        if self.dataset_type == DatasetType.INTERACTIONS:
            self.tokens = variable_definition.get("tokens", None)
            self.distinct = variable_definition.get("distinct", False)
            
            try:
                self.elementIDs = variable_definition["elementIDs"]
            except:
                err_msg = colored(f'EMMA Data-Wrangling Error: Variable definition [{self.name}] uses the interactions table but does not provide an elementIDs attribute'+\
                    '(make list empty if you wish to look at all elementIDs).', "red")
                raise ValueError(err_msg)
                
            self.type = variable_definition.get("type", None)
            self.source = variable_definition.get("source", None)
        else:
            self.tokens     = None
            self.distinct   = None
            self.elementIDs = None
            self.type       = None
            self.source     = None
        
        # * ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # * Get Events attributes if Events Variable
        # * Make none for attributes otherwise to avoid contamination
        # * ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        if self.dataset_type == DatasetType.EVENTS:
            self.sum = variable_definition.get("sum", None)
            self.count = variable_definition.get("count", None)
            self.filter_by = variable_definition.get("filter_by", None)
            self.healthTrackType = variable_definition.get("healthTrackType", None)
            self.completed = variable_definition.get("completed", False)
        else:
            self.sum             = None
            self.count           = None
            self.filter_by       = None 
            self.healthTrackType = None
            self.completed       = None

        # * ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # * Get reference attributes if reference Variable
        # * Make none for attributes otherwise to avoid contamination
        # * ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        if self.dataset_type == None:
            self.defined_variable_x = variable_definition.get("defined-variable-x", None)
            self.defined_variable_y = variable_definition.get("defined-variable-y", None)
        else:
            self.defined_variable_x = None
            self.defined_variable_y = None      
    
    def convert_to_daily(self, x_is_daily=False, y_is_daily=False):
        if self.day_of_week != -1:
            raise Exception("Unable to convert to daily when scope is not weekly. (day of week = {})".format(self.day_of_week))
        
        res = []
        day_of_week = 0
        for day in ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]:
            day_variable = copy.deepcopy(self)
            
            day_variable.day_of_week = day_of_week
            day_variable.name += '-' + day
            if x_is_daily:
                day_variable.defined_variable_x += '-' + day   
            if y_is_daily:
                day_variable.defined_variable_y += '-' + day            
            
            res.append(day_variable)
            day_of_week += 1
        
        return res
        
        
        
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

    try:
        name = variable_definition["name"]
    except:
        err_msg = colored(f'EMMA Data-Wrangling Error: Variable definition missing name attribute.', "red")
        raise NameError(err_msg)
    
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

# Last Edit on 5/31/2023 by Reagan Kelley
# Create implicit calculation to determine scope of reference variables (defined-variable calculations)
def create_variable_dictionary(filename):
    """Reads through a json file which contains variable definitions for EMMA calculations.

    Args:
        filename (string): This file must be in the same directory as the python scripts, otherwise its an absolute path

    Returns:
        Dict [string, Variable]: Returns all the variable definitions in the JSON file
    """

    variables = {}
    with open(os.path.realpath(os.path.dirname(__file__) + "/" + filename)) as json_file:
        data = json.load(json_file)
        variable_defs = data['Variables']

        for vd in variable_defs:
            variable_s = variable_factory(vd)
            for variable in variable_s:
                
                # * ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                # * Check to see if this is a defined-variable calculation
                # * and if so justify its scope.
                # * ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                if variable.day_of_week == -1:

                    x_is_daily = False
                    if (variable.defined_variable_x is not None):
                        # if defined_variable_x is a daily variable, get its day of the week variants
                        if variable.defined_variable_x not in variables.keys():
                            # no weekly or daily version of this variable name found, must be a mis-definition.
                            if variable.defined_variable_x + '-Monday' not in variables.keys():
                                err_msg = colored(f'EMMA Data-Wrangling Error: [{variable.name}] uses defined_variable_x, [{variable.defined_variable_x}], which is not a defined variable.', "red")
                                raise NameError(err_msg)
                            
                            x_is_daily = True

                    y_is_daily = False
                    if (variable.defined_variable_y is not None):
                        # if defined_variable_x is a daily variable, get its day of the week variants
                        if variable.defined_variable_y not in variables.keys():
                            # no weekly or daily version of this variable name found, must be a mis-definition.
                            if variable.defined_variable_y + '-Monday' not in variables.keys():
                                    err_msg = colored(f'EMMA Data-Wrangling Error: [{variable.name}] uses defined_variable_y, [{variable.defined_variable_y}], which is not a defined variable.', "red")
                                    raise NameError(err_msg)
                            
                            y_is_daily = True
                    
                    if x_is_daily or y_is_daily:
                        day_versions = variable.convert_to_daily(x_is_daily, y_is_daily)
                        for day_variable in day_versions:
                            variables[day_variable.name] = day_variable
                        continue
                                
                variables[variable.name] = variable
    return variables

if __name__ == "__main__":
    create_variable_dictionary("variable_definitions.json")