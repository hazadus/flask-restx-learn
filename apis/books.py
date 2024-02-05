from flask_restx import Namespace, Resource
from core.models import get_all_books

api = Namespace("books", description="Books related operations")


@api.route("/")
class BookList(Resource):
    @api.doc("list_books")
    def get(self):
        """List all books"""
        return get_all_books()
