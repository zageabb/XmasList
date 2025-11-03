from app.models import User
from tests.conftest import create_gift, create_user


def setup_users(app):
    with app.app_context():
        alice = create_user("alice@example.com", name="Alice")
        bob = create_user("bob@example.com", name="Bob")
    return alice, bob


def test_purchase_flow(client, app):
    alice, bob = setup_users(app)
    with app.app_context():
        gift = create_gift(alice, title="Camera")
        gift_id = gift.id

    client.post("/login", data={"email": "bob@example.com", "password": "password123"}, follow_redirects=True)
    response = client.post(f"/gifts/{gift_id}/purchase", follow_redirects=True)
    assert b"Gift marked as purchased" in response.data

    response = client.get("/me/purchases")
    assert b"Camera" in response.data

    response = client.post(f"/gifts/{gift_id}/unpurchase", follow_redirects=True)
    assert b"Purchase removed" in response.data


def test_cannot_purchase_own_gift(client, app):
    alice, _ = setup_users(app)
    with app.app_context():
        gift = create_gift(alice, title="Laptop")
        gift_id = gift.id

    client.post("/login", data={"email": "alice@example.com", "password": "password123"}, follow_redirects=True)
    response = client.post(f"/gifts/{gift_id}/purchase", follow_redirects=True)
    assert b"You cannot purchase your own gift" in response.data


def test_cannot_double_purchase(client, app):
    alice, bob = setup_users(app)
    with app.app_context():
        gift = create_gift(alice, title="Book")
        gift_id = gift.id

    client.post("/login", data={"email": "bob@example.com", "password": "password123"}, follow_redirects=True)
    client.post(f"/gifts/{gift_id}/purchase", follow_redirects=True)
    response = client.post(f"/gifts/{gift_id}/purchase", follow_redirects=True)
    assert b"You already purchased this gift" in response.data


def test_unpurchase_requires_buyer(client, app):
    alice, bob = setup_users(app)
    with app.app_context():
        gift = create_gift(alice, title="Watch")
        gift_id = gift.id

    client.post("/login", data={"email": "bob@example.com", "password": "password123"}, follow_redirects=True)
    client.post(f"/gifts/{gift_id}/purchase", follow_redirects=True)

    client.get("/logout", follow_redirects=True)
    with app.app_context():
        create_user("carol@example.com", name="Carol")
    client.post("/login", data={"email": "carol@example.com", "password": "password123"}, follow_redirects=True)
    response = client.post(f"/gifts/{gift_id}/unpurchase", follow_redirects=True)
    assert b"only unmark gifts you purchased" in response.data
