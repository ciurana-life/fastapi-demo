import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils.functions import create_database, database_exists

from app.auth.domain import create_access_token
from app.db.base import Base
from app.dependencies import get_db
from app.main import app
from app.users.crud import create_user
from app.users.schemas import UserCreate

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session")
def db_engine():
    if not database_exists:
        create_database(engine.url)

    Base.metadata.create_all(bind=engine)
    yield engine


@pytest.fixture(scope="function")
def db(db_engine):
    connection = db_engine.connect()
    # begin a non-ORM transaction
    transaction = connection.begin()
    # bind an individual Session to the connection
    db = TestingSessionLocal(bind=connection)
    yield db
    db.rollback()
    connection.close()


@pytest.fixture(scope="function")
def client(db):
    app.dependency_overrides[get_db] = lambda: db
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="session")
def token_header():
    token = create_access_token(username="sonja")
    yield {"Authorization": f"Bearer {token}"}


@pytest.fixture(scope="session")
def invalid_token_header():
    yield {"Authorization": "Bearer FHjf0934"}


@pytest.fixture
def db_user(db):
    create_user(
        db,
        UserCreate(
            email="admin@victorciurana.com",
            username="sonja",
            editable_field="some_data",
            password="victor",
        ),
    )
