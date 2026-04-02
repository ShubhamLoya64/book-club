"""
Pydantic request/response schemas with validation.

These schemas define the shape of API requests and responses.
They handle serialization, deserialization, and basic validation.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, field_validator


# ---------------------------------------------------------------------------
# User schemas
# ---------------------------------------------------------------------------

class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: str = Field(..., max_length=120)
    display_name: str = Field(..., min_length=1, max_length=100)


class UserCreate(UserBase):
    pass


class UserResponse(UserBase):
    id: int
    created_at: datetime

    model_config = {"from_attributes": True}


# ---------------------------------------------------------------------------
# Book schemas
# ---------------------------------------------------------------------------

class BookBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    author: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    published_date: Optional[str] = None
    isbn: Optional[str] = Field(None, max_length=13)
    page_count: Optional[int] = Field(None, gt=0)


class BookCreate(BookBase):
    """Schema for creating a new book."""

    @field_validator("published_date")
    @classmethod
    def validate_date_format(cls, v: Optional[str]) -> Optional[str]:
        """Validate the date string is in YYYY-MM-DD format."""
        if v is not None:
            try:
                datetime.strptime(v, "%Y-%m-%d")
            except ValueError:
                raise ValueError("published_date must be in YYYY-MM-DD format")
        return v


class BookUpdate(BaseModel):
    """Schema for updating a book. All fields optional."""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    author: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    published_date: Optional[str] = None
    isbn: Optional[str] = Field(None, max_length=13)
    page_count: Optional[int] = Field(None, gt=0)


class BookResponse(BookBase):
    id: int
    average_rating: float
    rating_count: int
    created_at: datetime

    model_config = {"from_attributes": True}


# ---------------------------------------------------------------------------
# Review schemas
# ---------------------------------------------------------------------------

class ReviewBase(BaseModel):
    rating: int
    text: str


class ReviewCreate(ReviewBase):
    """Schema for creating a review.

    Validation is handled in the service layer (services.py) to keep a single
    source of truth and return consistent 400 responses.
    """
    pass


class ReviewUpdate(BaseModel):
    rating: Optional[int] = Field(None, ge=1, le=5)
    text: Optional[str] = Field(None, min_length=1)


class ReviewResponse(ReviewBase):
    id: int
    user_id: int
    book_id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


# ---------------------------------------------------------------------------
# Reading List schemas
# ---------------------------------------------------------------------------

class ReadingListBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None


class ReadingListCreate(ReadingListBase):
    pass


class ReadingListResponse(ReadingListBase):
    id: int
    user_id: int
    created_at: datetime

    model_config = {"from_attributes": True}


class ReadingListItemCreate(BaseModel):
    book_id: int
    status: str = Field(default="unread")

    @field_validator("status")
    @classmethod
    def validate_status(cls, v: str) -> str:
        allowed = {"unread", "reading", "read"}
        if v not in allowed:
            raise ValueError(f"Status must be one of: {', '.join(sorted(allowed))}")
        return v


class ReadingListItemResponse(BaseModel):
    id: int
    book_id: int
    status: str
    date_added: datetime

    model_config = {"from_attributes": True}


class ReadingListDetailResponse(ReadingListResponse):
    """Reading list with its items included."""
    items: list[ReadingListItemResponse] = []

    model_config = {"from_attributes": True}
