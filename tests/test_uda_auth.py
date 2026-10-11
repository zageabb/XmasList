from app.models import User
from conftest import create_user


UDA_HEADERS = {"X-UDA-User": "proxy.user@example.com", "X-UDA-Groups": "Development,Personal"}


def enable_uda(app):
    app.config.update(UDA_AUTH_ENABLED=True, UDA_REQUIRED_GROUP="Development", UDA_USER_ALIASES={})


def test_trusted_proxy_identity_creates_and_signs_in_user(app, client):
    enable_uda(app)
    response = client.get("/", headers=UDA_HEADERS, environ_base={"REMOTE_ADDR": "127.0.0.1"})
    assert response.status_code == 302
    with app.app_context():
        user = User.query.filter_by(email="proxy.user@example.com").one()
        assert user.name == "Proxy User"


def test_direct_client_cannot_spoof_uda_identity(app, client):
    enable_uda(app)
    response = client.get("/", headers=UDA_HEADERS, environ_base={"REMOTE_ADDR": "192.168.1.50"})
    assert response.status_code == 200
    with app.app_context():
        assert User.query.filter_by(email="proxy.user@example.com").first() is None


def test_alias_maps_proxy_identity_to_existing_user(app, client):
    enable_uda(app)
    with app.app_context():
        existing = create_user("gerald@example.com", name="Gerald")
        existing_id = existing.id
    app.config["UDA_USER_ALIASES"] = {"uda@example.com": "gerald@example.com"}
    response = client.get(
        "/",
        headers={"X-UDA-User": "uda@example.com", "X-UDA-Groups": "Development"},
        environ_base={"REMOTE_ADDR": "127.0.0.1"},
    )
    assert response.status_code == 302
    with client.session_transaction() as session:
        assert session["_user_id"] == str(existing_id)
    with app.app_context():
        assert User.query.count() == 1


def test_required_group_is_enforced(app, client):
    enable_uda(app)
    response = client.get(
        "/",
        headers={"X-UDA-User": "proxy.user@example.com", "X-UDA-Groups": "Personal"},
        environ_base={"REMOTE_ADDR": "127.0.0.1"},
    )
    assert response.status_code == 200
