import json

from fastapi.testclient import TestClient


class TestUsersAPI:
    user_base = {
        "email": "admin@victorciurana.com",
        "username": "sonja",
        "editable_field": "some_data",
    }
    data = {**user_base, "password": "victor"}
    expected_response = {**user_base, "id": 1, "is_active": True}
    endpoint = "/api/v1/users/"

    def test_create_user(self, client: TestClient) -> None:
        response = client.post(self.endpoint, data=json.dumps(self.data))
        assert response.status_code == 200
        assert response.json() == self.expected_response

    def test_create_user_email_taken(self, db_user, client: TestClient) -> None:
        response = client.post(self.endpoint, data=json.dumps(self.data))
        assert response.status_code == 400
        assert response.json()["detail"] == "Email already registered"

    def test_create_user_username_taken(self, db_user, client: TestClient) -> None:
        data = {**self.data, "email": "another@email.com"}
        response = client.post(self.endpoint, data=json.dumps(data))
        assert response.status_code == 400
        assert response.json()["detail"] == "Username already registered"

    def test_read_user(self, db_user, token_header, client: TestClient) -> None:
        response = client.get(self.endpoint, headers=token_header)
        assert response.status_code == 200
        assert response.json() == self.expected_response

    def test_read_user_invalid_token(
        self, db_user, invalid_token_header, client: TestClient
    ) -> None:
        response = client.get(self.endpoint, headers=invalid_token_header)
        assert response.status_code == 401

    def test_read_user_no_user(self, token_header, client: TestClient) -> None:
        response = client.get(self.endpoint, headers=token_header)
        assert response.status_code == 404

    def test_update_user(self, db_user, token_header, client: TestClient) -> None:
        data = {"editable_field": "new_data"}
        response = client.put(
            self.endpoint, headers=token_header, data=json.dumps(data)
        )
        assert response.status_code == 200
        assert response.json() == {**self.expected_response, **data}

    def test_update_user_invalid_token(
        self, db_user, invalid_token_header, client: TestClient
    ) -> None:
        data = {"editable_field": "new_data"}
        response = client.put(
            self.endpoint, headers=invalid_token_header, data=json.dumps(data)
        )
        assert response.status_code == 401

    def test_update_user_no_user(self, token_header, client: TestClient) -> None:
        data = {"editable_field": "new_data"}
        response = client.put(
            self.endpoint, headers=token_header, data=json.dumps(data)
        )
        assert response.status_code == 404

    def test_delete_user(self, db_user, token_header, client: TestClient) -> None:
        response = client.delete(self.endpoint, headers=token_header)
        assert response.status_code == 200
        assert response.json() == {"ok": True}

    def test_delete_user_invalid_token(
        self, db_user, invalid_token_header, client: TestClient
    ) -> None:
        response = client.delete(self.endpoint, headers=invalid_token_header)
        assert response.status_code == 401

    def test_delete_user_no_user(self, token_header, client: TestClient) -> None:
        response = client.delete(self.endpoint, headers=token_header)
        assert response.status_code == 404
