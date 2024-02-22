from core.models import Book, BookSchema
from services.authors import create_author
from services.books import create_book, get_book, update_book


def create_book_and_author_from_payload(payload) -> Book:
    """
    Create new book (and new author if no author.id passed).
    :param payload: `{"title": "Book title", "author": {"id": 1}}` or
    `{"title": "Book title", "author": {"last_name": "Lastname", "first_name": "Firstname"}}`
    :return: newly created Book instance
    """
    book: dict = BookSchema().load(
        data=payload,
        # The only required field is book title
        partial={"id", "author.id", "author.last_name", "author.first_name"},
    )

    author_id = book["author"].id

    # If there's no author id in payload, then create new author and get its id
    if author_id is None:
        if len(book["author"].last_name) < 3:
            raise Exception(f"Author last name is too short.")

        if len(book["author"].first_name) < 3:
            raise Exception(f"Author first name is too short.")

        author = create_author(
            last_name=book["author"].last_name,
            first_name=book["author"].first_name,
            middle_name=book["author"].middle_name,
        )
        author_id = author.id

    return create_book(title=book["title"], author_id=author_id)


def create_book_and_author_from_payload_json(payload) -> dict:
    """
    Create new book (and new author if no author.id passed).
    :param payload: `{"title": "Book title", "author": {"id": 1}}` or
    `{"title": "Book title", "author": {"last_name": "Lastname", "first_name": "Firstname"}}`
    :return: JSON-serializable dict with newly created book data
    """
    book = create_book_and_author_from_payload(payload)
    return BookSchema().dump(book)


def update_or_create_book_from_payload_json(book_id: int, payload) -> (dict, int):
    """
    Update existing or create new book.
    :param book_id: book to update; if there's no book with such ID, new book will be created (ID will be assigned by database).
    :param payload: title field is required to update; title, author id | first + last name to create.
    :return: tuple of JSON-serializable updated book data and HTTP status code (200 or 201)
    """
    book_data = BookSchema().load(
        payload,
        partial={
            "id",
            "author.id",
            "author.last_name",
            "author.first_name",
            "author.middle_name",
        },
    )

    try:
        book = get_book(book_id)
        # Book exists - update it
        author = book_data.get("author", None)
        author_id = author.id if author else None
        book = update_book(book_id, title=book_data.get("title"), author_id=author_id)
        return BookSchema().dump(book), 200
    except:
        # Book does not exist - create it
        book = create_book_and_author_from_payload(payload)
        return BookSchema().dump(book), 201
