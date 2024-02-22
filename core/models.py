from dataclasses import dataclass
from typing import Optional

from marshmallow import Schema, fields, post_load


@dataclass
class Author:
    last_name: str
    first_name: str
    id: Optional[int] = None
    middle_name: Optional[str] = None


@dataclass
class Book:
    id: int
    title: str
    author: Author


class AuthorSchema(Schema):
    id = fields.Int()
    last_name = fields.Str(required=True)
    first_name = fields.Str(required=True)
    middle_name = fields.Str()

    @post_load
    def make_author(self, data, **kwargs):
        data["last_name"] = data.get("last_name", "")
        data["first_name"] = data.get("first_name", "")
        return Author(**data)


class BookSchema(Schema):
    id = fields.Int()
    title = fields.Str()
    author = fields.Nested(AuthorSchema)
