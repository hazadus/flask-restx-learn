from core.models import Book, BookSchema
from services.books import create_book


def create_book_and_author_from_payload(payload) -> Book:
    """
    TODO: this should create author in case it does not exist and no author.id passed.
    TODO: Write docstrings.

    :param payload:
    :return: newly created Book instance
    """
    book: dict = BookSchema().load(
        # NB: we don't require book id and author name in payload
        data=payload,
        partial={"id", "author.last_name", "author.first_name"},
    )
    return create_book(title=book["title"], author_id=book["author"].id)


def create_book_and_author_from_payload_json(payload) -> dict:
    """
    TODO: Write docstrings.
    :param payload:
    :return: JSON-serializable dict with newly created book data
    """
    book = create_book_and_author_from_payload(payload)
    return BookSchema().dump(book)
