# flask-restx-learn

Repo for experiments with Flask, oFlask-RESTX, Marshmallow and SQLAlchemy frameworks.

## References

- [Flask-RESTX Quick Start](https://flask-restx.readthedocs.io/en/latest/quickstart.html)
- [marshmallow docs](https://marshmallow.readthedocs.io/en/stable/)
  - [Partial loading](https://marshmallow.readthedocs.io/en/stable/quickstart.html#partial-loading)
  - [Handling unknown fields](https://marshmallow.readthedocs.io/en/stable/quickstart.html#handling-unknown-fields)
- [SQLAlchemy Unified Tutorial](https://docs.sqlalchemy.org/en/20/tutorial/index.html)
  - [Relationship Loading Techniques](https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html)
  - [Association Proxy](https://docs.sqlalchemy.org/en/20/orm/extensions/associationproxy.html)
  - [ORM Events](https://docs.sqlalchemy.org/en/14/orm/events.html)

## Repo Contents

- Minimal Flask-RESTX API: [minimal.py](minimal.py)
- Resourceful Routing Example: [resourceful.py](resourceful.py)
- Books API built using "[Scaling your project](https://flask-restx.readthedocs.io/en/latest/scaling.html)" example: 
  [books_app.py](books_app.py), featuring:
  - Flask-RESTX
  - Marshmallow
  - SQLite3
  - [Flasgger](https://github.com/flasgger/flasgger): API docs using external `yml` files (available at `/apidocs/` 
    route).
- SQLAlchemy basic examples: [alchemy/](alchemy/)
- SQLAlchemy + basic Flask CRUD API: [books_alchemy/](books_alchemy/)
