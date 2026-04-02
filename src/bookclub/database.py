"""
Database setup and session management.

Uses SQLite for development. The database file is created in the project root.
For testing, an in-memory SQLite database is used (see tests/conftest.py).
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

DATABASE_URL = "sqlite:///./bookclub.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models."""
    pass


def get_db():
    """
    Dependency that provides a database session.

    Yields a SQLAlchemy session and ensures it is closed after the request.
    Use this as a FastAPI dependency:

        @app.get("/example")
        def example(db: Session = Depends(get_db)):
            ...
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Create all database tables. Call once at startup."""
    Base.metadata.create_all(bind=engine)
