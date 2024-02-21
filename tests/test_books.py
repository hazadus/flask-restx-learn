import unittest

from books_app import app
from core.database import delete_db, init_db


class TestBooksEndpoint(unittest.TestCase):
    def setUp(self) -> None:
        delete_db()
        init_db()
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        self.app = app.test_client()
        self.base_url = "/api/books"

    def test_get_books_list(self):
        response = self.app.get(self.base_url + "/")
        self.assertEqual(response.status_code, 200)

    def test_get_author(self):
        response = self.app.get(self.base_url + "/1")
        self.assertIn("Clean Code", response.text)

    def test_delete_author(self):
        response = self.app.delete(self.base_url + "/0")
        self.assertEqual(response.status_code, 204)
