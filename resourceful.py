"""
Resourceful Routing
https://flask-restx.readthedocs.io/en/latest/quickstart.html#resourceful-routing

curl http://127.0.0.1:5000/todo1 -d "data=Remember the milk" -X PUT
curl http://127.0.0.1:5000/todo1
curl http://127.0.0.1:5000/todo2 -d "data=Change my brakepads" -X PUT
curl http://127.0.0.1:5000/todo2
"""

from http import HTTPStatus

from flask import Flask, request
from flask_restx import Api, Resource

app = Flask(__name__)
api = Api(app)

todos = {}


# api.add_resource(TodoSimple, "/<string:todo_id>")
# or
@api.route("/<string:todo_id>")
class TodoSimple(Resource):
    def get(self, todo_id):
        # Explicitly return HTTP code and custom headers:
        return (
            {todo_id: todos[todo_id]},
            HTTPStatus.OK,
            {"Etag": "some-opaque-string"},
        )

    def put(self, todo_id):
        todos[todo_id] = request.form["data"]
        return {todo_id: todos[todo_id]}


if __name__ == "__main__":
    app.run(debug=True)
