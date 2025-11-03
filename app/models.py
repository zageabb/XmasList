from __future__ import annotations

from datetime import datetime
from typing import Optional

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from .extensions import db, login_manager


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    name = db.Column(db.String(120), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    gifts = db.relationship("Gift", back_populates="owner", cascade="all, delete-orphan")
    purchases = db.relationship("Purchase", back_populates="buyer", cascade="all, delete-orphan")

    def __repr__(self) -> str:  # pragma: no cover - debug helper
        return f"<User {self.email}>"

    @property
    def username(self) -> str:
        return self.email.split("@")[0]

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)


class Gift(db.Model):
    __tablename__ = "gifts"

    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    url = db.Column(db.String(512))
    image_url = db.Column(db.String(512))
    image_path = db.Column(db.String(512))
    price = db.Column(db.Numeric(10, 2))
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    owner = db.relationship("User", back_populates="gifts")
    purchase = db.relationship("Purchase", back_populates="gift", uselist=False, cascade="all, delete-orphan")

    def purchased_by(self) -> Optional[User]:
        return self.purchase.buyer if self.purchase else None

    @property
    def is_purchased(self) -> bool:
        return self.purchase is not None

    def __repr__(self) -> str:  # pragma: no cover
        return f"<Gift {self.title}>"


class Purchase(db.Model):
    __tablename__ = "purchases"
    __table_args__ = (db.UniqueConstraint("gift_id", name="uq_purchases_gift"),)

    id = db.Column(db.Integer, primary_key=True)
    gift_id = db.Column(db.Integer, db.ForeignKey("gifts.id"), nullable=False, index=True)
    buyer_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    purchased_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    gift = db.relationship("Gift", back_populates="purchase")
    buyer = db.relationship("User", back_populates="purchases")

    def __repr__(self) -> str:  # pragma: no cover
        return f"<Purchase gift={self.gift_id} buyer={self.buyer_id}>"


@login_manager.user_loader
def load_user(user_id: str) -> Optional[User]:
    return User.query.get(int(user_id))
