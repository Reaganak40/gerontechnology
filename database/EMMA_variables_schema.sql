-- EMMA Variables SCHEMA
-- Last Modified By: Reagan Kelley

CREATE TABLE IF NOT EXISTS Participants
(
    participant_id INTEGER,
    first_name varchar(256),
    last_name varchar(256),

    PRIMARY KEY (participant_id)
);

CREATE TABLE IF NOT EXISTS Calculations
(
    participant_id INTEGER,
    week_number INTEGER,
    year_number INTEGER,

    -- Variables Used in the Calculations Table
    v_CalenderUse FLOAT,
    v_SumTotalCalendarInteractions FLOAT,
    v_CalendaringGoal FLOAT,
    v_TodayPageUse INT,
    v_SumTotalEventInteractions FLOAT,
    v_TodayPageGoal FLOAT,
    v_SumTotalLTGNoteInteractions FLOAT,
    v_LTGGoal INT,
    v_LTGFolderUse FLOAT,
    v_SumTotalFZNoteInteractions FLOAT,
    v_FZGoal INT,
    v_FZFolderUse FLOAT,
    v_TotalPEWeeklyPHEX INT,
    v_PEGoal FLOAT,
    v_TotalCEWeeklyMEEX INT,
    v_CEGoal FLOAT,
    v_TotalWEWeeklyWELLX INT,
    v_WEGoal FLOAT,
    
    PRIMARY KEY (participant_id, week_number, year_number),
    FOREIGN KEY (participant_id) REFERENCES Participants(participant_id)
);
    