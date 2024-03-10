"""
Establishing Connectivity - the Engine https://docs.sqlalchemy.org/en/20/tutorial/engine.html
Working with Transactions and the DBAPI https://docs.sqlalchemy.org/en/20/tutorial/dbapi_transactions.html
"""

from sqlalchemy import create_engine, text

engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)

with engine.connect() as conn:
    # Execute stuff and commit changes
    conn.execute(text("CREATE TABLE some_table (x int, y int)"))
    conn.execute(
        # NB: sending multiple parameters here:
        text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
        [
            {"x": 1, "y": 1},
            {"x": 2, "y": 4},
        ],
    )
    conn.commit()

    # Fetching rows
    result = conn.execute(text("SELECT x, y FROM some_table"))
    for row in result:
        print(f"{row=} {row.x=} {row.y=}")

    # Sending parameters
    result = conn.execute(text("SELECT x, y FROM some_table WHERE y > :y"), {"y": 2})
    for x, y in result:
        print(f"{x=} {y=}")
