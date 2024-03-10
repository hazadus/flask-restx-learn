"""
Using ORM Declarative Forms to Define Table Metadata https://docs.sqlalchemy.org/en/20/tutorial/metadata.html
Data Manipulation with the ORM https://docs.sqlalchemy.org/en/20/tutorial/orm_data_manipulation.html#tutorial-orm-data-manipulation
"""

from sqlalchemy import create_engine, ForeignKey, String, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session
from typing import List, Optional


engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user_account"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    fullname: Mapped[Optional[str]]
    addresses: Mapped[List["Address"]] = relationship(back_populates="user")

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"


class Address(Base):
    __tablename__ = "address"
    id: Mapped[int] = mapped_column(primary_key=True)
    email_address: Mapped[str]
    user_id = mapped_column(ForeignKey("user_account.id"))
    user: Mapped[User] = relationship(back_populates="addresses")

    def __repr__(self) -> str:
        return f"Address(id={self.id!r}, email_address={self.email_address!r})"


if __name__ == "__main__":
    # This will create all the tables:
    Base.metadata.create_all(engine)

    sandy = User(name="sandy", fullname="Sandy Rivers")

    with Session(engine) as session:
        # Actually insert new user into database:
        session.add(sandy)
        session.commit()

        # Find user in database by name:
        user = session.execute(select(User).filter_by(name="sandy")).scalar_one()
        print(user)

        # Update user in the database
        user.fullname = "Sandy Quievers"
        # Flush occurs automatically before any select, so we'll get the updated row:
        user = session.execute(select(User).filter_by(name="sandy")).scalar_one()
        print(user)

        # Delete user:
        session.delete(user)
        session.commit()
