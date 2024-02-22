from http import HTTPStatus

from flask_restx import Namespace, Resource

from services.books import delete_book, get_all_books_json, get_book_json
from services.common import create_book_and_author_from_payload_json

api = Namespace("books", description="Books related operations")


@api.route("/")
class BookList(Resource):
    @api.doc("list_books")
    def get(self):
        """List all books"""
        return get_all_books_json()

    @api.doc("create_book")
    def post(self):
        """Create new book (and author if needed), and return its data"""
        try:
            return (
                create_book_and_author_from_payload_json(api.payload),
                HTTPStatus.CREATED,
            )
        except Exception as ex:
            return api.abort(HTTPStatus.BAD_REQUEST, ex)


@api.route("/<book_id>")
@api.param("book_id", "The book identifier")
class Book(Resource):
    @api.doc("get_book")
    def get(self, book_id):
        """Get book by its id"""
        try:
            return get_book_json(book_id)
        except Exception:
            api.abort(HTTPStatus.NOT_FOUND, f"Book with {book_id=} not found.")

    @api.doc("delete_book")
    def delete(self, book_id):
        """Delete book by its id."""
        try:
            delete_book(book_id)
            return "", HTTPStatus.NO_CONTENT
        except Exception:
            api.abort(HTTPStatus.NOT_FOUND, f"Book with {book_id=} not found.")
