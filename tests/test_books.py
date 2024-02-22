import unittest
from http import HTTPStatus

from books_app import app
from core.database import INITIAL_AUTHORS, INITIAL_BOOKS, delete_db, init_db


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
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_get_book(self):
        book_id = INITIAL_BOOKS[0]["id"]
        book_title = INITIAL_BOOKS[0]["title"]

        response = self.app.get(self.base_url + "/" + str(book_id))
        self.assertIn(book_title, response.text)

    def test_delete_book(self):
        response = self.app.delete(self.base_url + "/0")
        self.assertEqual(response.status_code, HTTPStatus.NO_CONTENT)

    def test_post_book(self):
        """Ensure that book with existing author ID can be created."""
        book_title = "The New Book"
        author_id = INITIAL_AUTHORS[0]["id"]
        author_last_name = INITIAL_AUTHORS[0]["last_name"]
        author_first_name = INITIAL_AUTHORS[0]["first_name"]

        response = self.app.post(
            self.base_url + "/",
            json={"title": book_title, "author": {"id": author_id}},
        )

        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        self.assertIn(book_title, response.text)
        self.assertIn(author_last_name, response.text)
        self.assertIn(author_first_name, response.text)

    def test_post_book_with_wrong_author_id_fails(self):
        """Ensure that book can't be created with wrong author ID."""
        wrong_author_id = 42
        response = self.app.post(
            self.base_url + "/",
            json={"title": "The Book", "author": {"id": wrong_author_id}},
        )

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
