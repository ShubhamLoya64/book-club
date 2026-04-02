"""
Tests for review operations.

Test count: 7
"""


class TestReviews:
    """Tests for review CRUD operations."""

    def test_create_review(self, client, sample_user, sample_books):
        response = client.post(
            f"/books/{sample_books[0].id}/reviews",
            json={"rating": 4, "text": "Great book!"},
            headers={"Authorization": f"Bearer token-{sample_user.id}"},
        )
        assert response.status_code == 201
        data = response.json()
        assert data["rating"] == 4
        assert data["text"] == "Great book!"
        assert data["user_id"] == sample_user.id
        assert data["book_id"] == sample_books[0].id

    def test_create_review_requires_auth(self, client, sample_books):
        response = client.post(
            f"/books/{sample_books[0].id}/reviews",
            json={"rating": 4, "text": "Great book!"},
        )
        assert response.status_code == 401

    def test_create_review_invalid_rating(self, client, sample_user, sample_books):
        response = client.post(
            f"/books/{sample_books[0].id}/reviews",
            json={"rating": 6, "text": "Too high!"},
            headers={"Authorization": f"Bearer token-{sample_user.id}"},
        )
        assert response.status_code == 400

    def test_create_review_empty_text(self, client, sample_user, sample_books):
        response = client.post(
            f"/books/{sample_books[0].id}/reviews",
            json={"rating": 3, "text": ""},
            headers={"Authorization": f"Bearer token-{sample_user.id}"},
        )
        assert response.status_code == 400

    def test_list_reviews(self, client, sample_books, sample_review):
        response = client.get(f"/books/{sample_books[0].id}/reviews")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["rating"] == 5

    def test_create_duplicate_review(self, client, sample_user, sample_books, sample_review):
        """
        A user should not be able to review the same book twice.
        The service layer checks for an existing review and raises ValueError,
        which the route handler catches and returns as 400.
        """
        response = client.post(
            f"/books/{sample_books[0].id}/reviews",
            json={"rating": 3, "text": "Trying to review again"},
            headers={"Authorization": f"Bearer token-{sample_user.id}"},
        )
        assert response.status_code == 400
        assert "already reviewed" in response.json()["detail"].lower()

    def test_review_validation_consolidated(self, client, sample_user, sample_books):
        """
        Verify that review validation is consolidated in the service layer
        and returns a 400 with a simple string detail message.
        """
        response = client.post(
            f"/books/{sample_books[0].id}/reviews",
            json={"rating": 0, "text": "Testing validation consolidation"},
            headers={"Authorization": f"Bearer token-{sample_user.id}"},
        )
        # After consolidation, expect 400 with a clear string message
        assert response.status_code == 400, (
            f"Expected 400 from consolidated validation, got {response.status_code}. "
            f"Review validation is still scattered across schema (422), "
            f"route handler (400), and service layer (ValueError → 400)."
        )
        detail = response.json()["detail"]
        assert isinstance(detail, str), (
            f"Expected string error detail from consolidated validation, "
            f"got {type(detail).__name__}: {detail}"
        )
