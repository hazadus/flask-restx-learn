from dataclasses import dataclass

from marshmallow import Schema, fields


@dataclass
class Author:
    id: int
    last_name: str
    first_name: str
    middle_name: str


@dataclass
class Book:
    id: int
    title: str
    author: Author


class AuthorSchema(Schema):
    id = fields.Int()
    last_name = fields.Str()
    first_name = fields.Str()
    middle_name = fields.Str()


class BookSchema(Schema):
    id = fields.Int()
    title = fields.Str()
    author = fields.Nested(AuthorSchema)
