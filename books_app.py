from flask import Flask

from apis import api
from core.models import init_db, reset_db

app = Flask(__name__)
api.init_app(app)

reset_db()
init_db()
app.run(debug=True)
