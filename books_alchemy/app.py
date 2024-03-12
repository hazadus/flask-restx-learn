from http import HTTPStatus

from flask import Flask, abort, jsonify, request
from sqlalchemy.exc import NoResultFound

from books_alchemy.database import (
    Book,
    initialize_db,
    session,
    get_debtors,
    give_book,
    return_book,
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
    """
    Получить список должников, которые держат книги у себя более 14 дней (GET).
    curl -X GET http://127.0.0.1:5000/debtors/
    """
    debtors = []
    for student in get_debtors():
        debtors.append(student.to_json())
    return jsonify(debtors), HTTPStatus.OK


@app.route("/books/", methods=["POST"])
def post_give_book():
    """
    Выдать книгу студенту (POST — входные параметры ID книги и ID студента).
    curl -X POST -H "Content-Type: application/json" --data '{"book_id": 1, "student_id": 1}' http://127.0.0.1:5000/books/
    """
    book_id = request.json["book_id"]
    student_id = request.json["student_id"]
    gb = give_book(student_id=student_id, book_id=book_id)
    return gb.to_json(), HTTPStatus.CREATED


@app.route("/books/return/", methods=["POST"])
def post_return_book():
    """
    Сдать книгу в библиотеку (POST — входные параметры ID книги и ID студента, если такой связки нет, выдать ошибку).
    curl -X POST -H "Content-Type: application/json" --data '{"book_id": 1, "student_id": 1}' http://127.0.0.1:5000/books/return/
    """
    book_id = request.json["book_id"]
    student_id = request.json["student_id"]
    try:
        return_book(student_id=student_id, book_id=book_id)
        return "", HTTPStatus.OK
    except NoResultFound as ex:
        return f"Error: {ex}", HTTPStatus.NOT_FOUND


if __name__ == "__main__":
    initialize_db()
    app.run(debug=True)
