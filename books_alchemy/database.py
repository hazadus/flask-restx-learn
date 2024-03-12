import os.path
from datetime import datetime, timedelta

from sqlalchemy import (
    Boolean,
    Date,
    DateTime,
    Float,
    Integer,
    String,
    create_engine,
    select,
)
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker

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
    author_id: Mapped[int] = mapped_column(Integer, nullable=False)

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
    id: Mapped[int] = mapped_column(primary_key=True)
    book_id: Mapped[int] = mapped_column(Integer, nullable=False)
    student_id: Mapped[int] = mapped_column(Integer, nullable=False)
    date_of_issue: Mapped["DateTime"] = mapped_column(DateTime, nullable=False)
    date_of_return: Mapped["DateTime"] = mapped_column(
        DateTime, nullable=True, default=None
    )

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


def initialize_db():
    Base.metadata.create_all(engine)

    student1 = Student(
        id=1,
        name="Ivan",
        surname="Petrov",
        phone="+79210000001",
        email="ivan@petrov.ru",
        average_score=4.2,
        scholarship=False,
    )
    student2 = Student(
        id=2,
        name="Petr",
        surname="Ivanov",
        phone="+79210001000",
        email="petr@ivanov.ru",
        average_score=5.0,
        scholarship=True,
    )

    author1 = Author(id=1, name="Luciano", surname="Ramalho")
    book1 = Book(
        id=1,
        name="Fluent Python",
        count=1,
        release_date=datetime(2022, 3, 31),
        author_id=1,
    )
    given_book = GivenBook(
        book_id=1,
        student_id=1,
        date_of_issue=datetime(2024, 2, 27),
    )

    session.add_all([student1, student2, author1, book1, given_book])
    session.commit()


if __name__ == "__main__":
    initialize_db()
    print(list(Student.all_with_scholarship()))

    for student in Student.all_with_average_more_than(4.5):
        print(student[0].to_json())
