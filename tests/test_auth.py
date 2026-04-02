"""
Tests for authentication and rate limiting.
"""

from bookclub.auth import RateLimiter


class TestAuth:
    """Tests for token-based authentication."""

    def test_valid_token(self, client, sample_user):
        response = client.get(
            f"/users/{sample_user.id}",
            headers={"Authorization": f"Bearer token-{sample_user.id}"},
        )
        assert response.status_code == 200

    def test_no_token_on_public_endpoint(self, client, sample_user):
        """Public endpoints should work without auth."""
        response = client.get(f"/users/{sample_user.id}")
        assert response.status_code == 200

    def test_malformed_token(self, client, sample_books):
        response = client.post(
            f"/books/{sample_books[0].id}/reviews",
            json={"rating": 4, "text": "Good book"},
            headers={"Authorization": "Bearer bad-token"},
        )
        assert response.status_code == 401

    def test_missing_token_on_protected_endpoint(self, client, sample_books):
        """Review creation requires auth."""
        response = client.post(
            f"/books/{sample_books[0].id}/reviews",
            json={"rating": 4, "text": "Good book"},
        )
        assert response.status_code == 401


class TestRateLimiter:
    """Tests for the rate limiting middleware."""

    def test_rate_limiter_authenticated(self):
        """Authenticated requests should be rate limited by client token."""
        limiter = RateLimiter(max_requests=5, window_seconds=60)
        # Simulate an authenticated client
        bucket = limiter._get_or_create_bucket("token-1")
        assert bucket["count"] == 0

