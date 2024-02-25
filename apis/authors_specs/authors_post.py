authors_post_specs = {
    "tags": ["authors"],
    "description": "Create new author.",
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
        "Error": {
            "type": "object",
            "properties": {
                "message": {
                    "type": "string",
                }
            },
        },
    },
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "required": ["last_name", "first_name"],
                "properties": {
                    "last_name": {
                        "type": "string",
                        "required": True,
                    },
                    "first_name": {
                        "type": "string",
                        "required": True,
                    },
                    "middle_name": {
                        "type": "string",
                    },
                },
            },
        },
    ],
    "responses": {
        "201": {
            "description": "A new author created in the database",
            "schema": {
                "$ref": "#/definitions/Author",
            },
        },
        "400": {
            "description": "Bad request",
            "schema": {
                "$ref": "#/definitions/Error",
            },
        },
    },
}
