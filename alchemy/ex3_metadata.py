"""
Working with Database Metadata https://docs.sqlalchemy.org/en/20/tutorial/metadata.html
"""

from sqlalchemy import (
    MetaData,
    Table,
    Column,
    Integer,
    String,
    ForeignKey,
    create_engine,
)

engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)
metadata = MetaData()

user_table = Table(
    "user_account",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(32)),
    Column("full_name", String),
)

# Table column names:
print(user_table.c.keys())

# Single column info:
print(user_table.c.name)

address_table = Table(
    "address",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", ForeignKey("user_account.id"), nullable=False),
    Column("email", String, nullable=False),
)

# Emitting DDL to the Database (this will create all the tables):
metadata.create_all(engine)
