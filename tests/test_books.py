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
        self.assertEqual(HTTPStatus.OK, response.status_code)

    def test_get_book(self):
        book_id = INITIAL_BOOKS[0]["id"]
        book_title = INITIAL_BOOKS[0]["title"]

        response = self.app.get(self.base_url + "/" + str(book_id))
        self.assertIn(book_title, response.text)

    def test_delete_book(self):
        response = self.app.delete(self.base_url + "/0")
        self.assertEqual(HTTPStatus.NO_CONTENT, response.status_code)

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

        self.assertEqual(HTTPStatus.CREATED, response.status_code)
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

        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)

    def test_post_book_creates_new_author(self):
        book_id = INITIAL_BOOKS[0]["id"]
        book_title = "The New Book"
        author_last_name = "Ivanov"
        author_first_name = "Ivan"

        response = self.app.post(
            self.base_url + "/",
            json={
                "title": book_title,
                "author": {
                    "last_name": author_last_name,
                    "first_name": author_first_name,
                },
            },
        )

        self.assertEqual(HTTPStatus.CREATED, response.status_code)
        self.assertIn(book_title, response.text)
        self.assertIn(author_last_name, response.text)
        self.assertIn(author_first_name, response.text)

    def test_post_book_fails_create_new_author_with_short_name(self):
        """Ensure that author with len(last_name) < 3 and len(first_name) < 3 won't be created"""
        book_id = INITIAL_BOOKS[0]["id"]
        book_title = "The New Book"
        author_last_name = "I"
        author_first_name = "I"

        response = self.app.post(
            self.base_url + "/",
            json={
                "title": book_title,
                "author": {
                    "last_name": author_last_name,
                    "first_name": author_first_name,
                },
            },
        )

        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)

    def test_patch_book_updates_title(self):
        book_id = INITIAL_BOOKS[0]["id"]
        new_book_title = "Updated Book Title"

        response = self.app.patch(
            self.base_url + f"/{book_id}",
            json={
                "title": new_book_title,
            },
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertIn(new_book_title, response.text)

    def test_patch_book_updates_author(self):
        book_id = INITIAL_BOOKS[0]["id"]
        new_author_id = INITIAL_BOOKS[0]["author_id"] + 1

        response = self.app.patch(
            self.base_url + f"/{book_id}",
            json={
                "author": {
                    "id": new_author_id,
                }
            },
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)

    def test_patch_book_updates_title_and_author(self):
        book_id = INITIAL_BOOKS[0]["id"]
        new_book_title = "Updated Book Title"
        new_author_id = INITIAL_BOOKS[0]["author_id"] + 1

        response = self.app.patch(
            self.base_url + f"/{book_id}",
            json={
                "title": new_book_title,
                "author": {
                    "id": new_author_id,
                },
            },
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertIn(new_book_title, response.text)

    def test_put_book_creates_new_book(self):
        new_book_id = 100500
        book_title = "Brand New Book"
        author_last_name = "Newest"
        author_first_name = "News"

        response = self.app.put(
            self.base_url + f"/{new_book_id}",
            json={
                "title": book_title,
                "author": {
                    "last_name": author_last_name,
                    "first_name": author_first_name,
                },
            },
        )
        self.assertEqual(HTTPStatus.CREATED, response.status_code)
        self.assertIn(book_title, response.text)
        self.assertIn(author_last_name, response.text)
        self.assertIn(author_first_name, response.text)

    def test_put_book_updates_existing_book_title_and_author(self):
        book_id = INITIAL_BOOKS[0]["id"]
        new_book_title = "Updated Book Title"
        new_author_id = INITIAL_BOOKS[0]["author_id"] + 1

        response = self.app.put(
            self.base_url + f"/{book_id}",
            json={
                "title": new_book_title,
                "author": {
                    "id": new_author_id,
                },
            },
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertIn(new_book_title, response.text)

    def test_put_book_updates_existing_book_title(self):
        book_id = INITIAL_BOOKS[0]["id"]
        new_book_title = "Updated Book Title"

        response = self.app.put(
            self.base_url + f"/{book_id}",
            json={
                "title": new_book_title,
            },
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertIn(new_book_title, response.text)

    def test_put_book_updates_author(self):
        book_id = INITIAL_BOOKS[0]["id"]
        new_author_id = INITIAL_BOOKS[0]["author_id"] + 1

        response = self.app.put(
            self.base_url + f"/{book_id}",
            json={
                "author": {
                    "id": new_author_id,
                }
            },
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)
