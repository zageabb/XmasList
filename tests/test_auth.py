from tests.conftest import create_user
from app.models import User


def test_register_and_login(client, app):
    response = client.post(
        "/register",
        data={"name": "Alice", "email": "alice@example.com", "password": "password123", "confirm": "password123"},
        follow_redirects=True,
    )
    assert b"Welcome to GiftList" in response.data
    with app.app_context():
        assert User.query.filter_by(email="alice@example.com").count() == 1

    response = client.get("/logout", follow_redirects=True)
    assert b"You have been logged out" in response.data

    response = client.post(
        "/login",
        data={"email": "alice@example.com", "password": "password123"},
        follow_redirects=True,
    )
    assert b"Logged in successfully" in response.data


def test_login_failure(client, app):
    with app.app_context():
        create_user("alice@example.com", password="password123", name="Alice")
    response = client.post(
        "/login",
        data={"email": "alice@example.com", "password": "wrong"},
        follow_redirects=True,
    )
    assert b"Invalid credentials" in response.data
