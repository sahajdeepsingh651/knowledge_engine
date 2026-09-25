import sqlite3

cursor = sqlite3.connect("engine.db").cursor()
cursor.executescript("""
CREATE TABLE concepts(
        concept_id INTEGER PRIMARY KEY,
        name TEXT

    );
    CREATE TABLE hard_spots(
        hard_spot_id INTEGER PRIMARY KEY,
        topic_name TEXT,
        testing_goal_prompt TEXT

    );
    CREATE TABLE hard_spot_criteria(
        id INTEGER PRIMARY KEY,
        hard_spot_id INTEGER,
        concept_id INTEGER,
        condition_to_pass TEXT
    );
    CREATE TABLE ledger(
        id INTEGER,
        timestamp DATETIME,
        criterion_id INTEGER,
        outcome TEXT
    )
""")

cursor.commit()
