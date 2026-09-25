import sqlite3


def calculate_urgency(criterion_id):
    connection = sqlite3.connect("engine.db")
    cursor = connection.cursor()
    cursor.execute(
        """
                        SELECT outcome ,COUNT(*)
                        FROM ledger
                        WHERE criterion_id = ?
                        GROUP BY outcome
                         """,
        (criterion_id,),
    )
    results = cursor.fetchall()
    successes = 0
    failures = 0
    for row in results:
        if row[0] == "Held":
            successes = row[1]
        elif row[0] == "Failed":
            failures = row[1]
    print(f"Total Successes: {successes},Total Failures:{failures}")
    n_0 = 1.0
    alpha = 0.1
    beta = 0.2
    n_final = n_0 * ((1 - alpha) ** successes) * ((1 + beta) ** failures)
    print(f"Final forgetting rate{n_final}")


calculate_urgency(1)
