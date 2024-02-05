import os
import sqlite3
from typing import Optional

INITIAL_AUTHORS = [
    {"id": 1, "last_name": "Romalho", "first_name": "Luciano", "middle_name": ""},
    {"id": 2, "last_name": "Martin", "first_name": "Robert", "middle_name": "C."},
    {"id": 3, "last_name": "Fowler", "first_name": "Martin", "middle_name": ""},
]
INITIAL_BOOKS = [
    {"id": 0, "author_id": 1, "title": "Fluent Python"},
    {"id": 1, "author_id": 2, "title": "Clean Code"},
    {
        "id": 3,
        "author_id": 3,
        "title": "Refactoring. Improving the Design of Existing Code",
    },
]
DATABASE_FILE = "books.db"


def reset_db():
    """Delete database file, if exists."""
    if os.path.exists(DATABASE_FILE):
        os.remove(DATABASE_FILE)


def init_db() -> None:
    with sqlite3.connect(DATABASE_FILE) as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(
            """
            SELECT name FROM sqlite_master
            WHERE type='table' AND name='table_books'; 
            """
        )
        exists: Optional[tuple[str,]] = cursor.fetchone()
        # now in `exist` we have tuple with table name if table really exists in DB
        if not exists:
            cursor.executescript(
                """
                CREATE TABLE `authors` (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    last_name TEXT NOT NULL,
                    first_name TEXT, 
                    middle_name TEXT NULL
                )
                """
            )
            cursor.executescript(
                """
                CREATE TABLE `books` (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    author_id INTEGER NOT NULL ,
                    title TEXT,
                    FOREIGN KEY (author_id)
                        REFERENCES `authors` (id)
                        ON DELETE CASCADE 
                )
                """
            )
            cursor.executemany(
                """
                INSERT INTO `authors`
                (id, last_name, first_name, middle_name) VALUES (?, ?, ?, ?)
                """,
                [
                    (
                        item["id"],
                        item["last_name"],
                        item["first_name"],
                        item["middle_name"],
                    )
                    for item in INITIAL_AUTHORS
                ],
            )
            cursor.executemany(
                """
                INSERT INTO `books`
                (id, author_id, title) VALUES (?, ?, ?)
                """,
                [
                    (item["id"], item["author_id"], item["title"])
                    for item in INITIAL_BOOKS
                ],
            )


def get_all_books():
    with sqlite3.connect(DATABASE_FILE) as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(
            """
            SELECT books.id, books.title, authors.id, authors.last_name, authors.first_name, authors.middle_name
            FROM books
            JOIN authors ON  books.author_id = authors.id
            """
        )
        return [(*row,) for row in cursor.fetchall()]
