from http import HTTPStatus

from flask_restx import Namespace, Resource

from services.authors import (
    create_author_from_payload_json,
    delete_author,
    get_all_authors_json,
    get_author_json,
)
from services.books import get_books_by_author_json

api = Namespace("authors", description="Authors related operations")


@api.route("/")
class AuthorList(Resource):
    @api.doc("list_authors")
    def get(self):
        """List all authors"""
        return get_all_authors_json()

    @api.doc("create_author")
    def post(self):
        """Create new author, and return its data"""
        try:
            return create_author_from_payload_json(api.payload), HTTPStatus.CREATED
        except Exception as ex:
            return api.abort(HTTPStatus.BAD_REQUEST, ex)


@api.route("/<author_id>")
@api.param("author_id", "The author identifier")
class Author(Resource):
    @api.doc("get_author")
    def get(self, author_id):
        """Get author info and list of author's books by author's id"""
        try:
            author = get_author_json(author_id)
        except Exception:
            return api.abort(
                HTTPStatus.NOT_FOUND, f"Author with {author_id=} not found."
            )

        return {
            **author,
            "books": get_books_by_author_json(author_id),
        }

    @api.doc("delete_author")
    def delete(self, author_id):
        """Delete author by its id, and all books of this author."""
        try:
            delete_author(author_id)
            return "", HTTPStatus.NO_CONTENT
        except Exception:
            api.abort(HTTPStatus.NOT_FOUND, f"Author with {author_id=} not found.")
