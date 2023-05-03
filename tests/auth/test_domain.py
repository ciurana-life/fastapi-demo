import pytest
from fastapi.exceptions import HTTPException
from jose import jwt

from app.auth.domain import authenticate_user, token_required
from app.config import Settings

settings = Settings()


def test_token_exception():
    no_user_token = jwt.encode(
        {"sub": 23}, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    with pytest.raises(HTTPException) as exc:
        token_required(no_user_token)

    assert exc.value.detail == "Could not validate credentials"
    assert exc.value.status_code == 401


def test_authenticate_user_wrong_password(db, db_user):
    assert authenticate_user(db, "sonja", "WRONG") == False
