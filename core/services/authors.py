import sqlite3

from core.database import DATABASE_FILE_PATH
from core.models import Author, AuthorSchema


def get_all_authors() -> list[Author]:
    with sqlite3.connect(DATABASE_FILE_PATH) as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(
            """
            SELECT id, last_name, first_name, middle_name
            FROM authors
            """
        )
        return [Author(*row) for row in cursor.fetchall()]


def get_all_authors_json() -> list:
    authors = get_all_authors()
    return AuthorSchema().dump(authors, many=True)
