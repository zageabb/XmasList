"""Static mobile UX and proxy route smoke checks."""
from conftest import create_user
from flask import url_for


def test_authenticated_mobile_navigation(client, app):
    with app.app_context():
        create_user("mobile@example.com")
    client.post("/login", data={"email": "mobile@example.com", "password": "password123"})
    response = client.get("/me/gifts")
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert 'mobile-bottom-nav' in html
    assert '/me/gifts' in html
    assert '/gifts/create' in html


def test_mobile_photo_input_and_preview(client, app):
    with app.app_context():
        create_user("mobile@example.com")
    client.post("/login", data={"email": "mobile@example.com", "password": "password123"})
    response = client.get("/gifts/create")
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert 'accept="image/*"' in html
    assert 'gift-image-preview' in html


def test_proxy_prefix_mobile_links(client, app):
    app.config.update(UDA_AUTH_ENABLED=True, UDA_REQUIRED_GROUP="Development")
    headers = {
        "X-UDA-User": "mobile.proxy@example.com",
        "X-UDA-Groups": "Development",
        "X-Forwarded-Prefix": "/apps/xmas-list",
        "X-Forwarded-Host": "example.test",
        "X-Forwarded-Proto": "https",
    }
    response = client.get("/me/gifts", headers=headers, environ_base={"REMOTE_ADDR": "127.0.0.1"})
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert '/apps/xmas-list/gifts/create' in html
    assert '/apps/xmas-list/static/css/style.css' in html
