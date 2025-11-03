import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from flask import Flask

from app import create_app, db
from app.models import Gift, Purchase, User


@pytest.fixture()
def app() -> Flask:
    app = create_app("testing")
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app: Flask):
    return app.test_client()


@pytest.fixture()
def runner(app: Flask):
    return app.test_cli_runner()


def register(client, email="user@example.com", password="password123", name="User"):
    return client.post(
        "/register",
        data={"email": email, "password": password, "confirm": password, "name": name},
        follow_redirects=True,
    )


def login(client, email="user@example.com", password="password123"):
    return client.post("/login", data={"email": email, "password": password}, follow_redirects=True)


def create_gift(owner: User, title: str = "Toy", **kwargs) -> Gift:
    gift = Gift(owner=owner, title=title, **kwargs)
    db.session.add(gift)
    db.session.commit()
    return gift


def purchase_gift(gift: Gift, buyer: User) -> Purchase:
    purchase = Purchase(gift=gift, buyer=buyer)
    db.session.add(purchase)
    db.session.commit()
    return purchase


def create_user(email: str, password: str = 'password123', name: str = 'User') -> User:
    user = User(email=email, name=name)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return user
