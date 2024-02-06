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


def delete_author(author_id: int) -> None:
    """Delete author by its id, and all books of this author.
    :param author_id: id of the author to delete
    :raises Exception: if nothing was deleted
    """
    with sqlite3.connect(DATABASE_FILE_PATH) as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        result = cursor.execute(
            """
            DELETE FROM authors WHERE authors.id = $1
            """,
            [author_id],
        )
        if not result.rowcount:
            raise Exception(f"Nothing was deleted. Wrong {author_id=}?")


def get_author(author_id: int) -> Author:
    """Return Author with `author_id`
    :param author_id: id of the author to return
    :return: Author with `author_id`
    :raises Exception: if author with `author_id` was not found
    """
    with sqlite3.connect(DATABASE_FILE_PATH) as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(
            """
            SELECT id, last_name, first_name, middle_name
            FROM authors
            WHERE authors.id = $1
            """,
            [author_id],
        )
        row = cursor.fetchone()

        if not row:
            raise Exception(f"Author id={author_id} not found.")

        return Author(*row)


def get_author_json(author_id: int) -> dict:
    author = get_author(author_id)
    return AuthorSchema().dump(author)
