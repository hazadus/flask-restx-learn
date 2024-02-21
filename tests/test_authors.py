import unittest

from books_app import app
from core.database import delete_db, init_db


class TestAuthorsEndpoint(unittest.TestCase):
    def setUp(self) -> None:
        delete_db()
        init_db()
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        self.app = app.test_client()
        self.base_url = "/api/authors"

    def test_get_author_list(self):
        response = self.app.get(self.base_url + "/")
        self.assertEqual(response.status_code, 200)

    def test_get_author(self):
        response = self.app.get(self.base_url + "/1")
        self.assertIn("Luciano", response.text)
        self.assertIn("Romalho", response.text)

    def test_post_author(self):
        response = self.app.post(
            self.base_url + "/",
            json={"last_name": "Pushkin", "first_name": "Alexander"},
        )
        self.assertEqual(response.status_code, 201)
        self.assertIn("Pushkin", response.text)
        self.assertIn("Alexander", response.text)

    def test_delete_author(self):
        response = self.app.delete(self.base_url + "/2")
        self.assertEqual(response.status_code, 204)
