from __future__ import annotations

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from sqlalchemy.exc import IntegrityError

from ..extensions import db
from ..models import Gift, Purchase


purchases_bp = Blueprint("purchases", __name__, url_prefix="", template_folder="../templates/purchases")


@purchases_bp.route("/me/purchases")
@login_required
def my_purchases():
    purchases = (
        Purchase.query.filter_by(buyer_id=current_user.id)
        .join(Gift)
        .order_by(Purchase.purchased_at.desc())
        .all()
    )
    return render_template("purchases/my_purchases.html", purchases=purchases)


@purchases_bp.route("/gifts/<int:gift_id>/purchase", methods=["POST"])
@login_required
def purchase_gift(gift_id: int):
    gift = Gift.query.get_or_404(gift_id)
    if gift.owner_id == current_user.id:
        flash("You cannot purchase your own gift", "warning")
        return redirect(request.referrer or url_for("users.user_gifts", username=gift.owner.username))
    if gift.purchase and gift.purchase.buyer_id == current_user.id:
        flash("You already purchased this gift", "info")
        return redirect(request.referrer or url_for("users.user_gifts", username=gift.owner.username))
    purchase = Purchase(gift=gift, buyer=current_user)
    db.session.add(purchase)
    try:
        db.session.commit()
        flash("Gift marked as purchased!", "success")
    except IntegrityError:
        db.session.rollback()
        flash("This gift has already been purchased", "warning")
    return redirect(request.referrer or url_for("users.user_gifts", username=gift.owner.username))


@purchases_bp.route("/gifts/<int:gift_id>/unpurchase", methods=["POST"])
@login_required
def unpurchase_gift(gift_id: int):
    gift = Gift.query.get_or_404(gift_id)
    if not gift.purchase:
        flash("This gift is not marked as purchased", "info")
        return redirect(request.referrer or url_for("users.user_gifts", username=gift.owner.username))
    if gift.purchase.buyer_id != current_user.id:
        flash("You can only unmark gifts you purchased", "danger")
        return redirect(request.referrer or url_for("users.user_gifts", username=gift.owner.username))
    db.session.delete(gift.purchase)
    db.session.commit()
    flash("Purchase removed", "info")
    return redirect(request.referrer or url_for("users.user_gifts", username=gift.owner.username))
