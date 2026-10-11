"""Authenticate requests using identity asserted by the trusted UDA proxy."""
from __future__ import annotations

import secrets

from flask import current_app, g, request
from flask_login import current_user, login_user

from .extensions import db
from .models import User


def authenticate_uda_request() -> None:
    """Map a trusted UDA identity to a local GiftList user."""
    g.uda_authenticated = False
    if not current_app.config.get("UDA_AUTH_ENABLED"):
        return
    if request.remote_addr not in current_app.config["UDA_TRUSTED_PROXY_IPS"]:
        return

    asserted_email = (request.headers.get("X-UDA-User") or "").strip().casefold()
    if not _valid_email(asserted_email):
        return
    required_group = current_app.config.get("UDA_REQUIRED_GROUP")
    groups = {value.strip() for value in (request.headers.get("X-UDA-Groups") or "").split(",") if value.strip()}
    if required_group and required_group not in groups:
        return

    aliases = current_app.config.get("UDA_USER_ALIASES") or {}
    local_email = str(aliases.get(asserted_email, asserted_email)).strip().casefold()
    if not _valid_email(local_email):
        return

    user = User.query.filter_by(email=local_email).first()
    if user is None:
        user = User(email=local_email, name=_display_name(asserted_email))
        user.set_password(secrets.token_urlsafe(32))
        db.session.add(user)
        db.session.commit()
    if not current_user.is_authenticated or current_user.id != user.id:
        login_user(user)
    g.uda_authenticated = True
    g.uda_user = asserted_email


def _valid_email(value: str) -> bool:
    return len(value) <= 254 and value.count("@") == 1 and not any(char.isspace() for char in value)


def _display_name(email: str) -> str:
    local = email.split("@", 1)[0].replace(".", " ").replace("_", " ").strip()
    return local.title() or "GiftList user"
