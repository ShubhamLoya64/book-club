# BookClub API

A team book club service for tracking books, reading lists, and reviews. Built with Python, FastAPI, and SQLAlchemy.

## Features

- **Book catalog** — browse, search, and add books
- **Reading lists** — create and manage personal reading lists
- **Reviews** — rate and review books (1–5 stars)
- **Authentication** — simple token-based auth with rate limiting
- **Seed data** — ships with sample books, users, reviews, and lists for development

## Quick Start

### Prerequisites

- [uv](https://docs.astral.sh/uv/) (automatically manages the correct Python version)

### Setup

```bash
# Install dependencies
uv sync

# Start the dev server
uv run uvicorn bookclub.app:app --reload
```

Then open **http://localhost:8000/docs** for interactive API documentation.

### Running Tests

```bash
# Run all tests
uv run pytest -v

# Run a specific test file
uv run pytest tests/test_books.py -v

# Run a single test
uv run pytest tests/test_books.py::TestBookSearch -v
```

## Project Structure

```
src/bookclub/
├── app.py          # FastAPI application, routes, and middleware
├── auth.py         # Token-based authentication and rate limiting
├── database.py     # Database setup and session management (SQLite)
├── models.py       # SQLAlchemy ORM models
├── schemas.py      # Pydantic request/response schemas
├── services.py     # Business logic and database queries
└── seed_data.py    # Sample data for development
```

## Authentication

Public endpoints (browsing and searching books) require no authentication.

Authenticated endpoints use a simple bearer token scheme:

```
Authorization: Bearer token-<user_id>
```

For example, to act as user 1: `Authorization: Bearer token-1`

## Tech Stack

- **Python 3.10+**
- **FastAPI** — web framework
- **SQLAlchemy** — ORM
- **SQLite** — database
- **Pydantic** — data validation
- **pytest** — testing
- **uv** — dependency management

## License

See [LICENSE](LICENSE) for details.
