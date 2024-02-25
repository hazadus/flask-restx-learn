authors_delete_specs = {
    "tags": ["authors"],
    "description": "Delete author and all of its books.",
    "parameters": [
        {
            "name": "author_id",
            "in": "path",
            "required": True,
            "type": "number",
        },
    ],
    "definitions": {
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
        "204": {
            "description": "Author was deleted from the database",
        },
        "404": {
            "description": "Not found",
            "schema": {
                "$ref": "#/definitions/Error",
            },
        },
    },
}
