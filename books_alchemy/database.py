import os.path
import re
from datetime import datetime, timedelta
from typing import Tuple

from sqlalchemy import (
    Boolean,
    Date,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    create_engine,
    event,
    extract,
    func,
    select,
)
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    backref,
    mapped_column,
    relationship,
    sessionmaker,
)

# For in-memory database, use this config:
# engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)

DB_FILENAME = "books.db"
if os.path.exists(DB_FILENAME):
    os.remove(DB_FILENAME)
engine = create_engine(f"sqlite:///{DB_FILENAME}", echo=True)
Session = sessionmaker(bind=engine)
session = Session()


class Base(DeclarativeBase):
    def to_json(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Book(Base):
    __tablename__ = "books"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    count: Mapped[int] = mapped_column(Integer, default=1)
    release_date: Mapped["Date"] = mapped_column(Date, nullable=False)
    author_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("authors.id"), nullable=False
    )
    author = relationship(
        "Author", backref=backref("books", cascade="all, delete-orphan", lazy="select")
    )
    students = relationship("GivenBook", back_populates="book")

    def __repr__(self) -> str:
        return (
            f"Book(id={self.id}, name={self.name}, count={self.count}, "
            f"release_date={self.release_date}, author_id={self.author_id})"
        )


class Author(Base):
    __tablename__ = "authors"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    surname: Mapped[str] = mapped_column(String, nullable=False)

    def __repr__(self) -> str:
        return f"Author(id={self.id}, name={self.name}, surname={self.surname})"


class Student(Base):
    __tablename__ = "students"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    surname: Mapped[str] = mapped_column(String, nullable=False)
    phone: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False)
    average_score: Mapped["Float"] = mapped_column(Float, nullable=False)
    scholarship: Mapped["Boolean"] = mapped_column(Boolean, nullable=False)

    books = relationship("GivenBook", back_populates="student")

    def __repr__(self) -> str:
        return (
            f"Student(id={self.id}, name={self.name}, surname={self.surname}, "
            f"phone={self.phone}, email={self.email}, average_score={self.average_score}, "
            f"scholarship={self.scholarship})"
        )

    @staticmethod
    def all_with_scholarship():
        return session.execute(select(Student).filter_by(scholarship=True))

    @staticmethod
    def all_with_average_more_than(min_average: float):
        return session.execute(
            select(Student).filter(Student.average_score > min_average)
        )


class GivenBook(Base):
    __tablename__ = "receiving_books"
    book_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("books.id"), primary_key=True
    )
    student_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("students.id"), primary_key=True
    )
    date_of_issue: Mapped["DateTime"] = mapped_column(DateTime, nullable=False)
    date_of_return: Mapped["DateTime"] = mapped_column(
        DateTime, nullable=True, default=None
    )

    student = relationship("Student", back_populates="books")
    book = relationship("Book", back_populates="students")

    def __repr__(self) -> str:
        return (
            f"GivenBook(id={self.id}, book_id={self.book_id}, student_id={self.student_id}, "
            f"date_of_issue={self.date_of_issue}, date_of_return={self.date_of_return})"
        )

    @hybrid_property
    def count_date_with_book(self) -> int:
        """Количество дней, которые читатель держит/держал книгу у себя"""
        if self.date_of_return:
            return (self.date_of_return - self.date_of_issue).days
        return (datetime.now() - self.date_of_issue).days


def get_all_books():
    return session.query(Book).all()


def get_books_by_name(name: str):
    return session.query(Book).filter(Book.name.ilike(f"%{name}%"))


def get_debtors() -> list[Student]:
    """Получить список должников, которые держат книги у себя более 14 дней."""
    given_books = session.execute(
        select(GivenBook)
        .filter_by(date_of_return=None)
        .filter(GivenBook.date_of_issue < datetime.today() - timedelta(14))
    )
    students = []
    for gb in given_books:
        student_ = session.execute(
            select(Student).filter_by(id=gb[0].student_id)
        ).scalar_one()
        students.append(student_)
    return students


def give_book(student_id: int, book_id: int) -> GivenBook:
    """
    Выдать книгу студенту.
    :param student_id: ID студента
    :param book_id: ID книги
    :return: новый инстанс GivenBook
    """
    gb = GivenBook(book_id=book_id, student_id=student_id, date_of_issue=datetime.now())
    session.add(gb)
    session.commit()
    return gb


def return_book(student_id: int, book_id: int):
    """
    Сдать книгу в библиотеку (входные параметры ID книги и ID студента, если такой связки нет, выдать ошибку).
    :param student_id: ID студента
    :param book_id: ID книги
    """
    gb = session.execute(
        select(GivenBook).filter_by(
            student_id=student_id, book_id=book_id, date_of_return=None
        )
    ).scalar_one()
    gb.date_of_return = datetime.now()
    session.commit()


def get_remaining_authors_books(author_id: int) -> int:
    """Количество оставшихся в библиотеке книг по автору (входной параметр — ID автора)."""
    return session.query(func.sum(Book.count)).filter_by(author_id=author_id).scalar()


def get_average_books_given_this_month() -> float:
    """Получить среднее количество книг, которые студенты брали в этом месяце."""
    students_qty = session.query(Student).count()
    # Count books given this month
    given_book_count = (
        session.query(GivenBook)
        .filter(extract("year", GivenBook.date_of_issue) == datetime.now().year)
        .filter(extract("month", GivenBook.date_of_issue) == datetime.now().month)
        .count()
    )
    return given_book_count / students_qty


def get_top10_readers() -> list[Tuple[Student, int]]:
    """Получите ТОП-10 самых читающих студентов в этом году.
    :return: Список кортежей вида (студент, кол-во прочитанных книг) за текущий год, по убыванию
    количества прочитанных книг.
    """
    return (
        session.query(Student, func.count(GivenBook.book_id))
        .filter(extract("year", GivenBook.date_of_issue) == datetime.now().year)
        .outerjoin(GivenBook)
        .group_by(Student.id)
        .order_by(func.count(GivenBook.book_id).desc())
        .limit(10)
    )


def get_most_popular_book() -> Book:
    """
    Получить самую популярную книгу среди студентов, у которых средний балл больше 4.0.
    :return: инстанс книги, которую больше всего брали студенты со средним баллом >4.
    """
    row = (
        session.query(Book, func.count(GivenBook.book_id))
        .outerjoin(GivenBook)
        .outerjoin(Student)
        .group_by(GivenBook.book_id)
        .filter(Student.average_score > 4)
        .order_by(func.count(GivenBook.book_id).desc())
        .first()
    )
    # row will contain (Book, count,) tuple:
    return row[0]


def get_unread_books(student_id: int) -> list:
    """Получить список книг, которые студент не читал, при этом другие книги этого автора студент уже брал."""
    # Подзапрос: авторы которых брал студент
    taken_authors_query = (
        session.query(Author.id)
        .outerjoin(Book)
        .outerjoin(GivenBook)
        .filter(GivenBook.student_id == student_id)
        .subquery()
    )
    taken_books_query = (
        session.query(GivenBook.book_id)
        .filter(GivenBook.student_id == student_id)
        .subquery()
    )
    # Запрос: книги которые студент не брал, но с авторами, которых брал
    books = (
        session.query(Book)
        .filter(Book.author_id.in_(taken_authors_query))
        .filter(Book.id.not_in(taken_books_query))
        .all()
    )
    return books


def initialize_db():
    Base.metadata.create_all(engine)

    student1 = Student(
        id=1,
        name="Ivan",
        surname="Petrov",
        phone="+7(921)000-00-01",
        email="ivan@petrov.ru",
        average_score=4.2,
        scholarship=False,
    )
    student2 = Student(
        id=2,
        name="Petr",
        surname="Ivanov",
        phone="+7(921)000-10-00",
        email="petr@ivanov.ru",
        average_score=5.0,
        scholarship=True,
    )

    author1 = Author(name="Luciano", surname="Ramalho")
    book1 = Book(
        name="Fluent Python (2nd edition)",
        count=10,
        release_date=datetime(2022, 3, 31),
    )
    book2 = Book(
        name="Fluent Python (First edition)",
        count=2,
        release_date=datetime(2018, 1, 1),
    )
    author1.books.append(book1)
    author1.books.append(book2)

    author2 = Author(name="Brandon", surname="Rhodes")
    book3 = Book(
        name="Foundations of Python Network Programming",
        count=10,
        release_date=datetime(2014, 3, 2),
    )
    author2.books.append(book3)

    author3 = Author(name="Robert", surname="Martin")
    author3.books.append(
        Book(name="Clean Code", count=6, release_date=datetime(2008, 8, 1))
    )
    author3.books.append(
        Book(name="The Clean Coder", count=3, release_date=datetime(2017, 9, 1))
    )
    author3.books.append(
        Book(name="Clean Architecture", count=7, release_date=datetime(2017, 9, 1))
    )
    author3.books.append(
        Book(
            name="Clean Agile: Back to Basics",
            count=4,
            release_date=datetime(2019, 10, 1),
        )
    )

    session.add_all([student1, student2, author1, author2, author3])
    session.flush()

    given_book1 = GivenBook(
        book_id=book1.id,
        student_id=student1.id,
        date_of_issue=datetime(2024, 2, 1),
    )
    given_book2 = GivenBook(
        book_id=book3.id,
        student_id=student1.id,
        date_of_issue=datetime(2024, 3, 1),
    )
    given_book3 = GivenBook(
        book_id=book1.id,
        student_id=student2.id,
        date_of_issue=datetime(2024, 3, 10),
    )
    given_book4 = GivenBook(
        book_id=4,
        student_id=student2.id,
        date_of_issue=datetime(2024, 1, 12),
    )
    session.add_all([given_book1, given_book2, given_book3, given_book4])
    session.commit()


def before_insert_student_listener(mapper, connection, target: Student):
    if not re.search(r"^\+7\(9\d\d\)\d\d\d-\d\d-\d\d$", target.phone):
        raise ValueError(f"Wrong phone format: {target.phone}")


event.listen(Student, "before_insert", before_insert_student_listener)

if __name__ == "__main__":
    initialize_db()
    print(list(Student.all_with_scholarship()))

    for student in Student.all_with_average_more_than(4.5):
        print(student[0].to_json())

    for row in get_top10_readers():
        print(row)

    print(get_remaining_authors_books(author_id=1))

    print(get_most_popular_book())

    for book in get_unread_books(student_id=2):
        print(book)
