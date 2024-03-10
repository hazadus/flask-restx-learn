from sqlalchemy import create_engine, String, Integer, Date, Float, Boolean, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session


engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)


class Base(DeclarativeBase):
    pass


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


class GivenBook(Base):
    __tablename__ = "receiving_books"
    id: Mapped[int] = mapped_column(primary_key=True)
    book_id: Mapped[int] = mapped_column(Integer, nullable=False)
    student_id: Mapped[int] = mapped_column(Integer, nullable=False)
    date_of_issue: Mapped["DateTime"] = mapped_column(DateTime, nullable=False)
    date_of_return: Mapped["DateTime"] = mapped_column(DateTime, nullable=True)

    def __repr__(self) -> str:
        return (
            f"GivenBook(id={self.id}, book_id={self.book_id}, student_id={self.student_id}, "
            f"date_of_issue={self.date_of_issue}, date_of_return={self.date_of_return})"
        )


if __name__ == "__main__":
    # This will create all the tables:
    Base.metadata.create_all(engine)
