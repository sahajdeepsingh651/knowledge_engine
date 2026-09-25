import sqlite3

conn = sqlite3.connect("engine.db")
cursor = conn.cursor()
cursor.executescript(
    """
INSERT INTO concepts(concept_id,name)
VALUES(1,'OVS FLOW Caching');

INSERT INTO hard_spots(hard_spot_id,topic_name,testing_goal_prompt)
VALUES(1,'SB DB Failure','Test if existing traffic continues');


INSERT INTO hard_spot_criteria(id ,hard_spot_id,concept_id,condition_to_pass)
VALUES(1,1,1,'Must mention local caching');

INSERT INTO ledger (timestamp,criterion_id,outcome)
VALUES('2026-09-01 10:00:00',1 , 'Held');
INSERT INTO ledger(timestamp,criterion_id,outcome)
VALUES('2026-09-02 10:00:00', 1 , 'Failed');


        """
)
