from http import HTTPStatus

from flask_restx import Namespace, Resource

from core.services.authors import get_all_authors_json

api = Namespace("authors", description="Authors related operations")


@api.route("/")
class AuthorList(Resource):
    @api.doc("list_authors")
    def get(self):
        """List all authors"""
        return get_all_authors_json()
