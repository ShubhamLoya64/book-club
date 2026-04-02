"""
Tests for reading list operations.
"""


class TestReadingLists:
    """Tests for reading list CRUD operations."""

    def test_create_reading_list(self, client, sample_user):
        response = client.post(
            f"/users/{sample_user.id}/lists",
            json={"name": "My New List", "description": "Books to read"},
            headers={"Authorization": f"Bearer token-{sample_user.id}"},
        )
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "My New List"
        assert data["user_id"] == sample_user.id

    def test_create_reading_list_requires_auth(self, client, sample_user):
        response = client.post(
            f"/users/{sample_user.id}/lists",
            json={"name": "Unauthorized List"},
        )
        assert response.status_code == 401

    def test_create_reading_list_wrong_user(self, client, sample_users):
        """Can't create a list for another user."""
        response = client.post(
            f"/users/{sample_users[1].id}/lists",
            json={"name": "Not My List"},
            headers={"Authorization": f"Bearer token-{sample_users[0].id}"},
        )
        assert response.status_code == 403

    def test_get_reading_list(self, client, sample_user, sample_reading_list):
        response = client.get(
            f"/users/{sample_user.id}/lists/{sample_reading_list.id}"
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Horror Classics"
        assert len(data["items"]) == 3

    def test_add_book_to_list(self, client, sample_user, sample_books, sample_reading_list):
        response = client.post(
            f"/users/{sample_user.id}/lists/{sample_reading_list.id}/items",
            json={"book_id": sample_books[3].id, "status": "unread"},
            headers={"Authorization": f"Bearer token-{sample_user.id}"},
        )
        assert response.status_code == 201
        data = response.json()
        assert data["book_id"] == sample_books[3].id
        assert data["status"] == "unread"

    def test_add_duplicate_book_to_list(self, client, sample_user, sample_books, sample_reading_list):
        """Can't add the same book to a list twice."""
        response = client.post(
            f"/users/{sample_user.id}/lists/{sample_reading_list.id}/items",
            json={"book_id": sample_books[0].id, "status": "unread"},
            headers={"Authorization": f"Bearer token-{sample_user.id}"},
        )
        assert response.status_code == 409
