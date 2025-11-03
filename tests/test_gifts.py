from tests.conftest import create_gift, create_user, purchase_gift


def test_owner_cannot_see_purchase_status(client, app):
    with app.app_context():
        alice = create_user("alice@example.com", name="Alice")
        bob = create_user("bob@example.com", name="Bob")
        gift = create_gift(alice, title="Chess Set")
        purchase_gift(gift, bob)

    client.post("/login", data={"email": "alice@example.com", "password": "password123"}, follow_redirects=True)
    response = client.get("/me/gifts")
    assert b"badge bg-success" not in response.data
    assert b"Mark as Purchased" not in response.data


def test_non_owner_sees_purchase_status(client, app):
    with app.app_context():
        alice = create_user("alice@example.com", name="Alice")
        bob = create_user("bob@example.com", name="Bob")
        carol = create_user("carol@example.com", name="Carol")
        gift = create_gift(alice, title="Board Game")
        purchase_gift(gift, bob)

    client.post("/login", data={"email": "carol@example.com", "password": "password123"}, follow_redirects=True)
    response = client.get("/users/alice/gifts")
    assert b"badge bg-success" in response.data
    assert b"Mark as Purchased" not in response.data


def test_owner_cannot_edit_others_gift(client, app):
    with app.app_context():
        alice = create_user("alice@example.com", name="Alice")
        bob = create_user("bob@example.com", name="Bob")
        gift = create_gift(alice, title="Drone")
        gift_id = gift.id

    client.post("/login", data={"email": "bob@example.com", "password": "password123"}, follow_redirects=True)
    response = client.post(
        f"/gifts/{gift_id}/edit",
        data={"title": "Drone", "description": "", "url": "", "image_url": "", "price": "", "notes": ""},
        follow_redirects=True,
    )
    assert b"You cannot edit this gift" in response.data
