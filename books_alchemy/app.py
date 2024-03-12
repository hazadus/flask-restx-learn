from http import HTTPStatus

from flask import Flask, abort, jsonify, request

from books_alchemy.database import (
    Book,
    initialize_db,
    session,
    get_debtors,
)

app = Flask(__name__)


@app.route("/books/", methods=["GET"])
def get_all_books():
    """Получить все книги в библиотеке (GET)"""
    books = []
    for book in session.query(Book).all():
        books.append(book.to_json())
    return jsonify(books), HTTPStatus.OK


@app.route("/debtors/", methods=["GET"])
def get_debtors_list():
    """Получить список должников, которые держат книги у себя более 14 дней (GET)."""
    debtors = []
    for student in get_debtors():
        debtors.append(student.to_json())
    return debtors


# выдать книгу студенту (POST — входные параметры ID книги и ID студента)

# сдать книгу в библиотеку (POST — входные параметры ID книги и ID студента, если такой связки нет, выдать ошибку).

if __name__ == "__main__":
    initialize_db()
    app.run(debug=True)
