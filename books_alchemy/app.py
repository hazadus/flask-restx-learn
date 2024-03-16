from http import HTTPStatus

from flask import Flask, jsonify, request
from sqlalchemy.exc import NoResultFound

from books_alchemy.database import (
    get_all_books,
    get_average_books_given_this_month,
    get_books_by_name,
    get_debtors,
    get_most_popular_book,
    get_remaining_authors_books,
    get_top10_readers,
    get_unread_books,
    give_book,
    initialize_db,
    return_book,
)

app = Flask(__name__)


@app.route("/books/", methods=["GET"])
def get_all_books_route():
    """Получить все книги в библиотеке (GET)
    С параметром `?name=...` возвращает список книг, в названии которых содержится значение `name`.

    Examples:
        curl -X GET 'http://127.0.0.1:5000/books/?name=fluent'
    """
    if name := request.args.get("name", None):
        book_results = get_books_by_name(name=name)
    else:
        book_results = get_all_books()

    books = []
    for book in book_results:
        books.append(book.to_json())
    return jsonify(books), HTTPStatus.OK


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


@app.route("/books/average/", methods=["GET"])
def get_books_average():
    """Получить среднее количество книг, которые студенты брали в этом месяце."""
    result = {
        "average_books_given": get_average_books_given_this_month(),
    }
    return result, HTTPStatus.OK


@app.route("/books/most_popular/", methods=["GET"])
def get_most_popular_book_route():
    """
    Получить самую популярную книгу среди студентов, у которых средний балл больше 4.0.
    curl -X GET http://127.0.0.1:5000/books/most_popular/
    """
    book = get_most_popular_book()
    return book.to_json(), HTTPStatus.OK


@app.route("/books/unread/<student_id>/", methods=["GET"])
def get_unread_books_route(student_id):
    """
    Получить список книг, которые студент не читал, при этом другие книги этого автора студент уже брал.
    curl -X GET http://127.0.0.1:5000/books/unread/2/
    """
    result = []
    for book in get_unread_books(student_id=student_id):
        result.append(book.to_json())
    return result, HTTPStatus.OK


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


@app.route("/top10/", methods=["GET"])
def get_top10():
    """
    Получить ТОП-10 самых читающих студентов в этом году.
    curl -X GET http://127.0.0.1:5000/top10/
    """
    readers = []
    for row in get_top10_readers():
        readers.append(row[0].to_json())
    return jsonify(readers), HTTPStatus.OK


@app.route("/author/<author_id>/", methods=["GET"])
def get_remaining_authors_books_count(author_id):
    """
    Количество оставшихся в библиотеке книг по автору (входной параметр — ID автора)
    curl -X GET http://127.0.0.1:5000/author/1/
    """
    books_count = get_remaining_authors_books(author_id)
    result = {
        "author_id": author_id,
        "remaining_books_count": books_count,
    }
    return result, HTTPStatus.OK


if __name__ == "__main__":
    initialize_db()
    app.run(debug=True)
