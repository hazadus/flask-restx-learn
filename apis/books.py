from flask_restx import Namespace, Resource

api = Namespace("books", description="Books related operations")


@api.route("/")
class BookList(Resource):
    @api.doc("list_books")
    def get(self):
        """List all books"""
        return [{"id": 1, "title": "Fluent Python"}]
