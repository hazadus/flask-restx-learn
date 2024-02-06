from http import HTTPStatus

from flask_restx import Namespace, Resource

from services.authors import delete_author, get_all_authors_json

api = Namespace("authors", description="Authors related operations")


@api.route("/")
class AuthorList(Resource):
    @api.doc("list_authors")
    def get(self):
        """List all authors"""
        return get_all_authors_json()


@api.route("/<author_id>")
@api.param("author_id", "The author identifier")
class Author(Resource):
    @api.doc("delete_author")
    def delete(self, author_id):
        """Delete author by its id, and all books of this author."""
        try:
            delete_author(author_id)
            return "", HTTPStatus.NO_CONTENT
        except Exception:
            api.abort(HTTPStatus.NOT_FOUND, f"Author with {author_id=} not found.")
