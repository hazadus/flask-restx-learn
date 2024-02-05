from flask_restx import Api

from .books import api as api_books

api = Api(
    title="Books API",
    version="1.0",
    description="Simple books API built to test Flask-RESTX.",
)

api.add_namespace(api_books, path="/books")
