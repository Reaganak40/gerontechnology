import pandas as pd
import os
import sys
from pathlib import Path


def removePHI(filename, datatype):
    INPUT_FILE = Path(os.path.realpath(os.path.dirname(__file__))).joinpath(filename).absolute()
    
    # * ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # * Making checks on input file
    # * ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    if not INPUT_FILE.exists():
        err_msg = f"File does not exist: [{INPUT_FILE}]"
        raise FileNotFoundError(err_msg)
    
    if INPUT_FILE.suffix == ".csv":
        df = pd.read_csv(INPUT_FILE)
    elif INPUT_FILE.suffix == ".xlsx":
        df = pd.read_excel(INPUT_FILE)
    else:
        err_msg = f"removePHI: File type [{INPUT_FILE.suffix}] is not supported."
        raise FileNotFoundError(err_msg)
    
    if datatype == 'entries':
        for PHI_column in ['title', 'content']:
            if PHI_column not in df.columns:
                err_msg = f"removePHI: entries data file missing column {PHI_column}, determined unsafe for removePHI process."
                raise AttributeError(err_msg)
    elif datatype == 'events':
        for PHI_column in ['taskTitle', 'taskDescription']:
            if PHI_column not in df.columns:
                err_msg = f"removePHI: events data file missing column {PHI_column}, determined unsafe for removePHI process."
                raise AttributeError(err_msg)
    else:
        err_msg = f"{datatype} is not a supported datatype [this code should not run, this is a security concern]"
        raise NameError(err_msg)
        
    

def main(args):
    # * ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # * Command Line Argument Processing
    # * ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    try:
        file_index = args.index("--filename") + 1
        filename = args[file_index]
    except:
        err_msg = "removePHI requires arguments: [--filename 'relative/path/to/file']"
        raise Exception(err_msg)
    
    try:
        type_index = args.index("--type") + 1
        datatype = str.lower(args[type_index])
    except:
        err_msg = "removePHI requires arguments: [--type 'entries OR events']"
        raise Exception(err_msg)
    
    if (datatype not in ['entries', 'events']):
        err_msg = f"removePHI argument --type '{datatype}' not supported." 
        raise Exception(err_msg)
    
    removePHI(filename, datatype)
    

if __name__ == '__main__':
    main(sys.argv[1:])