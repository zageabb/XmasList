from app.models import Gift
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


def test_create_gift_infers_image_url(client, app, monkeypatch):
    with app.app_context():
        user = create_user("dave@example.com", name="Dave")

    def fake_infer(url: str) -> str | None:
        assert url == "https://example.com/widget"
        return "https://cdn.example.com/widget.jpg"

    monkeypatch.setattr("app.gifts.routes.infer_image_url", fake_infer)

    client.post("/login", data={"email": "dave@example.com", "password": "password123"}, follow_redirects=True)

    client.post(
        "/gifts/create",
        data={
            "title": "Widget",
            "description": "",
            "url": "https://example.com/widget",
            "image_url": "",
            "price": "",
            "notes": "",
        },
        follow_redirects=True,
    )

    with app.app_context():
        gift = Gift.query.filter_by(title="Widget").one()
        assert gift.image_url == "https://cdn.example.com/widget.jpg"


def test_infer_image_url_parses_meta(monkeypatch):
    from app.utils.images import infer_image_url

    class FakeResponse:
        headers = {"Content-Type": "text/html; charset=utf-8"}
        text = """<html><head><meta property='og:image' content='/img/prod.jpg'></head></html>"""
        url = "https://shop.example.com/item"

        def raise_for_status(self):
            return None

    def fake_get(url, timeout=5, headers=None):
        assert url == "https://shop.example.com/item"
        return FakeResponse()

    monkeypatch.setattr("app.utils.images.requests.get", fake_get)

    result = infer_image_url("https://shop.example.com/item")
    assert result == "https://shop.example.com/img/prod.jpg"
