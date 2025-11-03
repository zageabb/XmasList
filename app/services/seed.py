from __future__ import annotations

from datetime import datetime

from flask import current_app

from ..extensions import db
from ..models import Gift, Purchase, User


def seed_demo_data() -> None:
    """Populate the database with demo users and gifts."""
    if not current_app:
        raise RuntimeError("Seed must be run within an application context")

    existing_users = User.query.count()
    if existing_users:
        current_app.logger.info("Seed skipped: users already exist")
        return

    alice = User(email="alice@example.com", name="Alice")
    alice.set_password("password123")

    bob = User(email="bob@example.com", name="Bob")
    bob.set_password("password123")

    carol = User(email="carol@example.com", name="Carol")
    carol.set_password("password123")

    db.session.add_all([alice, bob, carol])
    db.session.flush()

    gifts = [
        Gift(owner=alice, title="LEGO Star Wars", description="Millennium Falcon set", url="https://lego.com/"),
        Gift(owner=alice, title="Wool Scarf", notes="Blue color", price=29.99),
        Gift(owner=bob, title="Cookbook", description="Holiday recipes"),
        Gift(owner=carol, title="Noise Cancelling Headphones", url="https://example.com/headphones"),
    ]
    db.session.add_all(gifts)
    db.session.flush()

    purchase = Purchase(gift=gifts[0], buyer=bob)
    db.session.add(purchase)

    db.session.commit()
    current_app.logger.info("Demo data seeded")
