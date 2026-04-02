"""
Test fixtures for the BookClub API.

Provides:
    - An in-memory SQLite database for test isolation
    - A test client configured with the test DB
    - Pre-seeded test data (a few users, books, reviews, and lists)
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from bookclub.database import Base, get_db
from bookclub.models import Book, ReadingList, ReadingListItem, Review, User


# Use an in-memory SQLite database for tests, shared across connections via StaticPool
engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)


# Enable foreign keys for SQLite
@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(autouse=True)
def setup_database():
    """Create all tables before each test and drop them after."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client():
    """Provide a test HTTP client with test DB overrides."""
    from bookclub.app import app

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app, raise_server_exceptions=False) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture
def db():
    """Provide a database session for direct DB manipulation in tests."""
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def sample_user(db) -> User:
    """Create and return a sample user."""
    user = User(
        username="testuser",
        email="test@example.com",
        display_name="Test User",
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def sample_users(db) -> list[User]:
    """Create and return multiple sample users."""
    users = [
        User(username="alice", email="alice@example.com", display_name="Alice Smith"),
        User(username="bob", email="bob@example.com", display_name="Bob Jones"),
        User(username="charlie", email="charlie@example.com", display_name="Charlie Brown"),
    ]
    for user in users:
        db.add(user)
    db.commit()
    for user in users:
        db.refresh(user)
    return users


@pytest.fixture
def sample_books(db) -> list[Book]:
    """
    Create and return sample books.

    Includes books designed to trigger the search duplication bug:
    - Stephen King books where "king" appears in author and description
    - A book with "King" in the title from a different author
    """
    books = [
        Book(
            title="The Shining",
            author="Stephen King",
            description="A family heads to an isolated hotel. A masterwork by King.",
            published_date="1977-01-28",
            isbn="9780385121675",
            page_count=447,
        ),
        Book(
            title="It",
            author="Stephen King",
            description="A group of children confront a shapeshifting monster. King's epic tale.",
            published_date="1986-09-15",
            isbn="9780670813025",
            page_count=1138,
        ),
        Book(
            title="Dune",
            author="Frank Herbert",
            description="An epic tale of politics on the desert planet Arrakis.",
            published_date="1965-08-01",
            isbn="9780441172719",
            page_count=688,
        ),
        Book(
            title="1984",
            author="George Orwell",
            description="A dystopian masterpiece about totalitarianism.",
            published_date="1949-06-08",
            isbn="9780451524935",
            page_count=328,
        ),
        Book(
            title="To Kill a Mockingbird",
            author="Harper Lee",
            description="A young girl witnesses racial injustice in the American South.",
            published_date="1960-07-11",
            isbn="9780061120084",
            page_count=281,
        ),
        Book(
            title="The King of Elfland's Daughter",
            author="Lord Dunsany",
            description="A classic fantasy novel about a prince who ventures beyond the fields we know.",
            published_date="1924-01-01",
            isbn="9780345431929",
            page_count=240,
        ),
    ]
    for book in books:
        db.add(book)
    db.commit()
    for book in books:
        db.refresh(book)
    return books


@pytest.fixture
def sample_review(db, sample_user, sample_books) -> Review:
    """Create and return a sample review."""
    review = Review(
        user_id=sample_user.id,
        book_id=sample_books[0].id,
        rating=5,
        text="Absolutely terrifying. King at his best.",
    )
    db.add(review)
    db.commit()
    db.refresh(review)
    return review


@pytest.fixture
def sample_reading_list(db, sample_user, sample_books) -> ReadingList:
    """Create a reading list with some items."""
    reading_list = ReadingList(
        user_id=sample_user.id,
        name="Horror Classics",
        description="The scariest books ever written",
    )
    db.add(reading_list)
    db.commit()
    db.refresh(reading_list)

    # Add a couple of books
    for i, book in enumerate(sample_books[:3]):
        status = ["read", "reading", "unread"][i]
        item = ReadingListItem(
            reading_list_id=reading_list.id,
            book_id=book.id,
            status=status,
        )
        db.add(item)
    db.commit()
    db.refresh(reading_list)
    return reading_list
