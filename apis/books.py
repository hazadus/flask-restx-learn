from http import HTTPStatus

from flask_restx import Namespace, Resource

from core.services import get_all_books_json, get_book_by_id_json

api = Namespace("books", description="Books related operations")


@api.route("/")
class BookList(Resource):
    @api.doc("list_books")
    def get(self):
        """List all books"""
        return get_all_books_json()


@api.route("/<book_id>")
@api.param("book_id", "The book identifier")
class Book(Resource):
    @api.doc("get_book")
    def get(self, book_id):
        """Get book by its id"""
        try:
            return get_book_by_id_json(book_id)
        except Exception:
            api.abort(HTTPStatus.NOT_FOUND, f"Book with {book_id=} not found.")
