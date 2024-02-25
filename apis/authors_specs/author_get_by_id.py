authors_get_by_id_specs = {
    "tags": ["authors"],
    "description": "Get author info and list of author's books by author's ID.",
    "parameters": [
        {
            "name": "author_id",
            "in": "path",
            "required": True,
            "type": "number",
        },
    ],
    "definitions": {
        "Author": {
            "type": "object",
            "properties": {
                "id": {
                    "type": "number",
                },
                "last_name": {
                    "type": "string",
                },
                "first_name": {
                    "type": "string",
                },
                "middle_name": {
                    "type": "string",
                },
            },
        },
        "Book": {
            "type": "object",
            "properties": {
                "id": {
                    "type": "number",
                },
                "title": {
                    "type": "string",
                },
                "author": {
                    "$ref": "#/definitions/Author",
                },
            },
        },
        "Error": {
            "type": "object",
            "properties": {
                "message": {
                    "type": "string",
                }
            },
        },
    },
    "responses": {
        "200": {
            "description": "Author info and list of author's books by author's ID.",
            "schema": {
                "type": "object",
                "properties": {
                    "id": {
                        "type": "number",
                    },
                    "last_name": {
                        "type": "string",
                    },
                    "first_name": {
                        "type": "string",
                    },
                    "middle_name": {
                        "type": "string",
                    },
                    "books": {
                        "type": "array",
                        "items": {"$ref": "#/definitions/Book"},
                    },
                },
            },
        },
        "404": {
            "description": "Not found",
            "schema": {
                "$ref": "#/definitions/Error",
            },
        },
    },
}
