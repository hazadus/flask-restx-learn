from flask import Flask

from apis import api
from core.database import delete_db, init_db

app = Flask(__name__)
api.init_app(app)

delete_db()
init_db()
app.run(debug=True)
