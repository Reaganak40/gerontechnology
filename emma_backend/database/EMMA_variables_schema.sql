-- EMMA Variables SCHEMA
-- This is a base schema, variable columns are added dynamically later.

CREATE TABLE IF NOT EXISTS Participants
(
    participant_id INTEGER,
    participant_name varchar(256),
    study varchar(10),
    cohort int,
    active int,

    PRIMARY KEY (participant_id)
);

CREATE TABLE IF NOT EXISTS Calculations
(
    participant_id INTEGER,
    week_number INTEGER,
    year_number INTEGER,
    
    PRIMARY KEY (participant_id, week_number, year_number),
    FOREIGN KEY (participant_id) REFERENCES Participants(participant_id)
);
    