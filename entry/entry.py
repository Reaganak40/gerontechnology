import json
import subprocess
import os
import datetime
import time
from colorama import just_fix_windows_console
from termcolor import colored
from pathlib import Path

just_fix_windows_console()

logs = ""
def log(start, timestamp, msg):
    global logs
    end = time.time()
    log_timestamp = f"[Log][{timestamp} +{round(end-start)}] "
    print(colored(log_timestamp, "blue"), end='')
    print(msg)
    logs += log_timestamp + msg + "\n"

def update_log_txt():
    global logs
    if os.path.isfile("log.txt"):
        logs = "\n" + logs
    with open("log.txt", 'a+') as f:
        f.write(logs)

def terminate(start, timestamp):
    global logs
    log(start, timestamp, "EMMA Backend session ended prematurely.")
    update_log_txt()
    exit()


def try_run_python(command):
    try:
        subprocess.run(command, shell=True, check=True, capture_output=True)
    except subprocess.CalledProcessError as err:
        err_msg = err.stderr.decode('utf8').replace("\n", "")[:-1]
        log(start, timestamp, f"{command[1]} encountered an error: {err_msg}")
        terminate(start, timestamp)

# Get time of execution
start = time.time()
timestamp = str(datetime.datetime.now()).replace(":", ".")

log(start, timestamp, "New EMMA Backend session started.")

# read config settings
f = open('config.json')
data = json.load(f)
f.close()


entries = ""
events = ""
interactions = ""
for file in os.listdir(os.getcwd()):
    if file.startswith("entries"):
        if len(entries) != 0:
            log(start, timestamp, "Error: Found multiple entries files in directory.")
            terminate(start, timestamp)
            
        entries = file
    elif file.startswith("events"):
        if len(events) != 0:
            log(start, timestamp, "Error: Found multiple events files in directory.")
            terminate(start, timestamp)
            
        events = file
    elif file.startswith("interactions"):
        if len(interactions) != 0:
            log(start, timestamp, "Error: Found multiple interactions files in directory.")
            terminate(start, timestamp)
        interactions = file


if len(entries) == 0:
    log(start, timestamp, "Error: Could not locate entries dataset in directory.")
    terminate(start, timestamp)
elif len(events) == 0:
    log(start, timestamp, "Error: Could not locate events dataset in directory.")
    terminate(start, timestamp)
elif len(interactions) == 0:
    log(start, timestamp, "Error: Could not locate interactions dataset in directory.")
    terminate(start, timestamp)

log(start, timestamp, "Entries/Events/Interaction datasets found.")

# Run removePHI on entries
try_run_python(["python", "removePHI.py", "--filename", entries, "--type", "entries"])
log(start, timestamp, f"Removed PHI from dataset: {entries}")

# Run removePHI on events
try_run_python(["python", "removePHI.py", "--filename", events, "--type", "events"])
log(start, timestamp, f"Removed PHI from dataset: {events}")


# Move PHI files to safe directory
safe_path = os.path.normpath(os.path.join(os.getcwd(), data["PHI_path"], timestamp).replace("/", "\\"))
os.mkdir(safe_path)
Path(entries).rename(os.path.join(safe_path, entries))
Path(events).rename(os.path.join(safe_path, events))
log(start, timestamp, f"Moved PHI files to: {safe_path}")


# Move NoPHI files to data wrangling
data_wrangling_input_path = os.path.normpath(os.path.join(os.getcwd(), data["emma_backend_path"], "data_wrangling/data/input", timestamp).replace("/", "\\"))
os.mkdir(data_wrangling_input_path)

for file in os.listdir(os.getcwd()):
    if file.startswith("entries"):
        entries_noPHI = file
    elif file.startswith("events"):
        events_noPHI = file
        
Path(entries_noPHI).rename(os.path.join(data_wrangling_input_path, entries_noPHI))
Path(events_noPHI).rename(os.path.join(data_wrangling_input_path, events_noPHI))
Path(interactions).rename(os.path.join(data_wrangling_input_path, interactions))

log(start, timestamp, f"Moved filtered datasets to: {data_wrangling_input_path}")

log(start, timestamp, "Starting data-wrangling pipeline...")

# run data-wrangling pipeline
emma_backend_py = os.path.normpath(os.path.join(os.getcwd(), data["emma_backend_path"], "emma_backend.py").replace("/", "\\"))
entries_noPHI = os.path.join(timestamp, entries_noPHI)
events_noPHI = os.path.join(timestamp, events_noPHI)
interactions = os.path.join(timestamp, interactions)

try_run_python(["python", emma_backend_py,
                "--interactions", interactions, "--events", events_noPHI, "--entries", entries_noPHI,
                "--debug", "1", "--research", "1",
                "--db_host", data["db_host"], "--db_username", data["db_username"], "--db_password", data["db_password"]])

log(start, timestamp, "EMMA Backend session ended successfully.")

update_log_txt()