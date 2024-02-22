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


def get_books_by_author(author_id: int) -> list[Book]:
    with sqlite3.connect(DATABASE_FILE_PATH) as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(
            """
            SELECT books.id, books.title, authors.id, authors.last_name, authors.first_name, authors.middle_name
            FROM books
            JOIN authors ON  books.author_id = authors.id
            WHERE authors.id = $1
            """,
            [author_id],
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


def get_books_by_author_json(author_id: int) -> list:
    books = get_books_by_author(author_id)
    return BookSchema().dump(books, many=True)


def get_book(book_id: int) -> Book:
    """Return Book with `book_id`
    :param book_id: id of the book to return
    :return: Book with `book_id`
    :raises Exception: if book with `book_id` was not found
    """
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


def get_book_json(book_id: int) -> str:
    book = get_book(book_id)
    return BookSchema().dump(book)


def create_book(title: str, author_id: int) -> Book:
    new_book_id = None

    with sqlite3.connect(DATABASE_FILE_PATH) as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        result = cursor.execute(
            """
            INSERT INTO `books`
            (author_id, title) VALUES (?, ?)
            """,
            [author_id, title],
        )
        if not result.rowcount:
            raise Exception("Book was not created.")

        new_book_id = result.lastrowid

    return get_book(book_id=new_book_id)


def update_book(
    book_id: int, title: str | None = None, author_id: int | None = None
) -> Book:
    """
    Update book title, author ID, or both.
    :param book_id: book to update
    :param title: new book title to set
    :param author_id: new author ID to set
    :return: updated `Book` instance
    """
    book = get_book(book_id)

    new_title = title if title is not None else book.title
    new_author_id = author_id if author_id is not None else book.author.id

    with sqlite3.connect(DATABASE_FILE_PATH) as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        result = cursor.execute(
            """
            UPDATE `books`
            SET `author_id` = ?, `title` = ?
            WHERE `id` = ?
            """,
            [new_author_id, new_title, book_id],
        )
        if not result.rowcount:
            raise Exception("Book was not updated.")

    book.title = new_title
    book.author.id = new_author_id

    return book


def update_book_from_payload_json(book_id: int, payload) -> dict:
    """
    Update book title, author ID, or both.
    :param book_id: book to update
    :param payload: example - `{"title": "New title", "author": {"id": 1}}`.
    :return: JSON-serializable updated book data
    """
    book = BookSchema().load(payload, partial=True)
    author_id = None

    if author := book.get("author", None):
        author_id = author.id

    updated_book = update_book(
        book_id,
        title=book.get("title", None),
        author_id=author_id,
    )
    return BookSchema().dump(updated_book)


def delete_book(book_id: int) -> None:
    """Delete book by its id.
    :param book_id: id of the book to delete
    :raises Exception: if nothing was deleted
    """
    with sqlite3.connect(DATABASE_FILE_PATH) as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        result = cursor.execute(
            """
            DELETE FROM books WHERE books.id = $1
            """,
            [book_id],
        )
        if not result.rowcount:
            raise Exception(f"Nothing was deleted. Wrong {book_id=}?")
