from tests.conftest import create_gift, create_user


def test_user_search(client, app):
    with app.app_context():
        create_user("alice@example.com", name="Alice Wonderland")
        create_user("bob@example.com", name="Bob Builder")

    client.post("/login", data={"email": "alice@example.com", "password": "password123"}, follow_redirects=True)
    response = client.get("/users?q=builder")
    body = response.data
    assert b"Bob Builder" in body
    assert b"/users/bob/gifts" in body
    assert b"/users/alice/gifts" not in body


def test_view_user_gifts_respects_privacy(client, app):
    with app.app_context():
        alice = create_user("alice@example.com", name="Alice")
        create_gift(alice, title="Sneakers")

    client.post("/login", data={"email": "alice@example.com", "password": "password123"}, follow_redirects=True)
    response = client.get("/users/alice/gifts")
    assert b"Mark as Purchased" not in response.data
