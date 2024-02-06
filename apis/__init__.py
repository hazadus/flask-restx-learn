from flask_restx import Api

from .authors import api as api_authors
from .books import api as api_books

api = Api(
    title="Books API",
    version="1.0",
    description="Simple books API built to test Flask-RESTX and Marshmallow.",
)

api.add_namespace(api_books, path="/api/books")
api.add_namespace(api_authors, path="/api/authors")
