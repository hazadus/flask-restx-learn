"""
Executing with an ORM Session https://docs.sqlalchemy.org/en/20/tutorial/dbapi_transactions.html
"""

from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session

engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)

with Session(engine) as session:
    # Execute SQL and commit changes
    session.execute(text("CREATE TABLE some_table (x int, y int)"))
    session.execute(
        # NB: sending multiple parameters here:
        text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
        [
            {"x": 1, "y": 1},
            {"x": 2, "y": 4},
        ],
    )
    session.commit()
