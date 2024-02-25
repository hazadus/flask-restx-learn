from http import HTTPStatus

from flask_restx import Namespace, Resource

from services.books import (
    delete_book,
    get_all_books_json,
    get_book_json,
    update_book_from_payload_json,
)
from services.common import (
    create_book_and_author_from_payload_json,
    update_or_create_book_from_payload_json,
)

api = Namespace("books", description="Books related operations")


@api.route("/")
class BookList(Resource):
    def get(self):
        """
        file: books_get_list.yml
        """
        return get_all_books_json()

    def post(self):
        """
        file: books_create.yml
        """
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
    def get(self, book_id):
        """
        file: books_get_by_id.yml
        """
        try:
            return get_book_json(book_id)
        except Exception:
            api.abort(HTTPStatus.NOT_FOUND, f"Book with {book_id=} not found.")

    def patch(self, book_id):
        """
        file: books_patch.yml
        """
        try:
            return update_book_from_payload_json(book_id, api.payload)
        except Exception as ex:
            return api.abort(HTTPStatus.BAD_REQUEST, ex)

    def put(self, book_id):
        """
        file: books_put.yml
        """
        try:
            json, status_code = update_or_create_book_from_payload_json(
                book_id, api.payload
            )
            return json, status_code
        except Exception as ex:
            return api.abort(HTTPStatus.BAD_REQUEST, ex)

    def delete(self, book_id):
        """
        file: books_delete.yml
        """
        try:
            delete_book(book_id)
            return "", HTTPStatus.NO_CONTENT
        except Exception:
            api.abort(HTTPStatus.NOT_FOUND, f"Book with {book_id=} not found.")
