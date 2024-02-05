import sqlite3

from core.database import DATABASE_FILE_PATH
from core.models import Author, Book, BookSchema


def get_all_books() -> list[Book]:
    with sqlite3.connect(DATABASE_FILE_PATH) as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(
            """
            SELECT books.id, books.title, authors.id, authors.last_name, authors.first_name, authors.middle_name
            FROM books
            JOIN authors ON  books.author_id = authors.id
            """
        )
        results = []
        for row in cursor.fetchall():
            (
                book_id,
                book_title,
                author_id,
                author_last_name,
                author_first_name,
                author_middle_name,
            ) = row
            results.append(
                Book(
                    id=book_id,
                    title=book_title,
                    author=Author(
                        id=author_id,
                        last_name=author_last_name,
                        first_name=author_first_name,
                        middle_name=author_middle_name,
                    ),
                )
            )
        return results


def get_all_books_json() -> list:
    books = get_all_books()
    return BookSchema().dump(books, many=True)


def get_book_by_id(book_id: int) -> Book:
    with sqlite3.connect(DATABASE_FILE_PATH) as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(
            """
            SELECT books.id, books.title, authors.id, authors.last_name, authors.first_name, authors.middle_name
            FROM books
            JOIN authors ON books.author_id = authors.id
            WHERE books.id = $1
            """,
            [book_id],
        )
        row = cursor.fetchone()

        if not row:
            raise Exception(f"Book id={book_id} not found.")

        (
            book_id,
            book_title,
            author_id,
            author_last_name,
            author_first_name,
            author_middle_name,
        ) = row
        return Book(
            id=book_id,
            title=book_title,
            author=Author(
                id=author_id,
                last_name=author_last_name,
                first_name=author_first_name,
                middle_name=author_middle_name,
            ),
        )


def get_book_by_id_json(book_id: int) -> str:
    book = get_book_by_id(book_id)
    return BookSchema().dump(book)
