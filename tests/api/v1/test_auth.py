from fastapi.testclient import TestClient


def test_get_access_token(db_user, client: TestClient) -> None:
    login_data = {
        "username": "sonja",
        "password": "victor",
    }
    response = client.post(f"/api/v1/token", data=login_data)
    tokens = response.json()
    assert response.status_code == 200
    assert "access_token" in tokens
    assert tokens["access_token"]


def test_get_access_token_unauthorized(client: TestClient) -> None:
    login_data = {
        "username": "sonja",
        "password": "WRONG",
    }
    response = client.post(f"/api/v1/token", data=login_data)
    assert response.status_code == 401
    assert response.json() == {"detail": "Incorrect username or password"}
