import sys
import glob
import os
import pandas as pd

def concat_excel(dirname, local):
    if(local):
        INPUT_DIR = os.getcwd() + R'\..\data\input' + "\\" + dirname
    else:
        INPUT_DIR = dirname
    csv_files = glob.glob(os.path.join(INPUT_DIR, "*.csv"))
    
    print(csv_files[0])
    concat_df = pd.read_csv(csv_files[0])

    for csv_index in range(1, len(csv_files)):
        print(csv_files[csv_index])
        df = pd.read_csv(csv_files[csv_index])
        concat_df = pd.concat([concat_df, df], verify_integrity=True, ignore_index=True)

    concat_df.to_csv(INPUT_DIR + R"\Cohort 1 Events_6mo_noPHI.csv", index=False)



def main():
    dirname_index = sys.argv.index("--dirname") + 1

    local = True
    try:
        local_index = sys.argv.index("--local") + 1
        if(int(sys.argv[local_index]) == 0):
            local = False
    except:
        pass

    concat_excel(sys.argv[dirname_index], local)



if __name__ == "__main__":
    main()