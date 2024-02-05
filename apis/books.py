from flask_restx import Namespace, Resource

from core.services import get_all_books_json

api = Namespace("books", description="Books related operations")


@api.route("/")
class BookList(Resource):
    @api.doc("list_books")
    def get(self):
        """List all books"""
        return get_all_books_json()
