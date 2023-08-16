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
    
    

# Get time of execution
start = time.time()
timestamp = str(datetime.datetime.now()).replace(":", ".")

log(start, timestamp, "New Data-Wrangling session started.")

# read config settings
f = open('config.json')
data = json.load(f)
f.close()


entries = ""
events = ""
interactions = ""
for file in os.listdir(os.getcwd()):
    if file.startswith("entries"):
        entries = file
    elif file.startswith("events"):
        events = file
    elif file.startswith("interactions"):
        interactions = file

log(start, timestamp, "Entries/Events/Interaction datasets found.")

# Run removePHI on entries
subprocess.run(["python", "removePHI.py", "--filename", entries, "--type", "entries"])
log(start, timestamp, f"Removed PHI from dataset: {entries}")

# Run removePHI on events
subprocess.run(["python", "removePHI.py", "--filename", events, "--type", "events"])
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

subprocess.run(["python", emma_backend_py,
                "--interactions", interactions, "--events", events_noPHI, "--entries", entries_noPHI,
                "--debug", "0", "--research", "1",
                "--db_host", data["db_host"], "--db_username", data["db_username"], "--db_password", data["db_password"]])

log(start, timestamp, "Data-wrangling session complete.")

with open("log.txt", 'a+') as f:
    f.write(logs)