"""
A minimal Flask-RESTX API

curl http://127.0.0.1:5000/hello
"""

from flask import Flask
from flask_restx import Resource, Api

app = Flask(__name__)
api = Api(app)


@api.route("/hello")
class HelloWorld(Resource):
    def get(self):
        return {"message": "Hello RestX world!"}


if __name__ == "__main__":
    app.run(debug=True)
