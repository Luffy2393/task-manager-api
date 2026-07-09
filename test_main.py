import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from main import app
from database import Base, get_db

TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


client = TestClient(app)

def test_register_user():
    response = client.post(
        "/auth/register",
        json={"email": "test@example.com", "password": "test1234"},
    )
    assert response.status_code == 200
    assert response.json()["email"] == "test@example.com"

def register_and_login(email: str, password: str) -> str:
    register_response = client.post(
        "/auth/register", json={"email": email, "password": password}
    )

    login_response = client.post(
        "/auth/login",
        data={"username": email, "password": password},
    )
    return login_response.json()["access_token"]

def test_user_access_another_users_task():
    token_a = register_and_login("usera@example.com", "passwordA")
    headers_a = {"Authorization": f"Bearer {token_a}"}

    create_response = client.post(
        "/tasks",
        json={"title": "User A's private task"},
        headers=headers_a,
    )
    task_id = create_response.json()["id"]

    token_b = register_and_login("userb@example.com", "passwordB")
    headers_b = {"Authorization": f"Bearer {token_b}"}

    response = client.get(f"/tasks/{task_id}", headers=headers_b)
    assert response.status_code == 404
