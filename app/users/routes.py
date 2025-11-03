from __future__ import annotations

from flask import Blueprint, abort, render_template, request
from flask_login import current_user, login_required

from ..models import Gift, User


users_bp = Blueprint("users", __name__, url_prefix="/users", template_folder="../templates/users")


@users_bp.route("")
@login_required
def list_users():
    query = request.args.get("q", "").strip()
    users = User.query
    if query:
        q = f"%{query}%"
        users = users.filter((User.name.ilike(q)) | (User.email.ilike(q)))
    users = users.order_by(User.created_at.asc()).all()
    return render_template("users/list.html", users=users, query=query)


@users_bp.route("/<string:username>/gifts")
@login_required
def user_gifts(username: str):
    user = User.query.filter(User.email.ilike(f"{username}@%"))
    user = user.order_by(User.created_at.asc()).first()
    if not user:
        abort(404)
    is_owner = current_user.is_authenticated and current_user.id == user.id
    gifts = Gift.query.filter_by(owner_id=user.id).order_by(Gift.created_at.asc()).all()
    return render_template("users/user_gifts.html", user=user, gifts=gifts, show_purchases=not is_owner)
