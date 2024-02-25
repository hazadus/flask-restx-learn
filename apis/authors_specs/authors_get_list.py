authors_get_list_specs = {
    "tags": ["authors"],
    "description": "Get list of all authors in the database.",
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
    },
    "responses": {
        "200": {
            "description": "A list of all authors in the database",
            "schema": {
                "type": "array",
                "items": {"$ref": "#/definitions/Author"},
            },
        },
    },
}
