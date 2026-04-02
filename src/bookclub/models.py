"""
SQLAlchemy ORM models for the BookClub API.

Models:
    - User: A registered user of the book club
    - Book: A book in the catalog
    - Review: A user's review of a book (rating + text)
    - ReadingList: A named collection of books belonging to a user
    - ReadingListItem: A book entry within a reading list, with reading status
"""

import datetime

from sqlalchemy import (
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship

from bookclub.database import Base


class User(Base):
    """A registered BookClub user."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(120), unique=True, nullable=False)
    display_name = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    reviews = relationship("Review", back_populates="user", cascade="all, delete-orphan")
    reading_lists = relationship(
        "ReadingList", back_populates="user", cascade="all, delete-orphan"
    )


class Book(Base):
    """A book in the catalog."""

    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False, index=True)
    author = Column(String(200), nullable=False, index=True)
    description = Column(Text, nullable=True)
    published_date = Column(String(10), nullable=True)  # stored as "YYYY-MM-DD"
    isbn = Column(String(13), unique=True, nullable=True)
    page_count = Column(Integer, nullable=True)
    average_rating = Column(Float, default=0.0)
    rating_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    reviews = relationship("Review", back_populates="book", cascade="all, delete-orphan")


class Review(Base):
    """A user's review of a book."""

    __tablename__ = "reviews"
    __table_args__ = (
        UniqueConstraint("user_id", "book_id", name="unique_user_book_review"),
    )

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    rating = Column(Integer, nullable=False)  # 1-5
    text = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    user = relationship("User", back_populates="reviews")
    book = relationship("Book", back_populates="reviews")


class ReadingList(Base):
    """A named reading list belonging to a user."""

    __tablename__ = "reading_lists"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="reading_lists")
    items = relationship(
        "ReadingListItem", back_populates="reading_list", cascade="all, delete-orphan"
    )


class ReadingListItem(Base):
    """A book entry within a reading list."""

    __tablename__ = "reading_list_items"
    __table_args__ = (
        UniqueConstraint(
            "reading_list_id", "book_id", name="unique_list_book"
        ),
    )

    id = Column(Integer, primary_key=True, index=True)
    reading_list_id = Column(Integer, ForeignKey("reading_lists.id"), nullable=False)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    status = Column(String(20), default="unread")  # unread, reading, read
    date_added = Column(DateTime, default=datetime.datetime.utcnow)

    reading_list = relationship("ReadingList", back_populates="items")
    book = relationship("Book")
