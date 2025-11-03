from __future__ import annotations

from decimal import Decimal
from pathlib import Path

from flask import (Blueprint, current_app, flash, redirect, render_template,
                   request, send_from_directory, url_for)
from flask_login import current_user, login_required

from ..extensions import db
from ..models import Gift
from ..utils.images import fetch_image, save_upload
from .forms import GiftForm


gifts_bp = Blueprint("gifts", __name__, url_prefix="", template_folder="../templates/gifts")


@gifts_bp.route("/dashboard")
@login_required
def dashboard():
    gifts = Gift.query.filter_by(owner_id=current_user.id).order_by(Gift.created_at.desc()).all()
    return render_template("dashboard.html", gifts=gifts)


@gifts_bp.route("/me/gifts")
@login_required
def my_gifts():
    gifts = Gift.query.filter_by(owner_id=current_user.id).order_by(Gift.created_at.desc()).all()
    return render_template("gifts/my_gifts.html", gifts=gifts)


@gifts_bp.route("/gifts/create", methods=["GET", "POST"])
@login_required
def create_gift():
    form = GiftForm()
    if form.validate_on_submit():
        gift = Gift(
            owner=current_user,
            title=form.title.data,
            description=form.description.data,
            url=form.url.data,
            image_url=form.image_url.data,
            price=Decimal(str(form.price.data)) if form.price.data is not None else None,
            notes=form.notes.data,
        )
        if form.image_file.data:
            try:
                gift.image_path = save_upload(form.image_file.data)
            except ValueError as exc:
                flash(str(exc), "danger")
                return render_template("gifts/gift_form.html", form=form, gift=None)
        db.session.add(gift)
        db.session.commit()
        flash("Gift created", "success")
        return redirect(url_for("gifts.my_gifts"))
    return render_template("gifts/gift_form.html", form=form, gift=None)


@gifts_bp.route("/gifts/<int:gift_id>/edit", methods=["GET", "POST"])
@login_required
def edit_gift(gift_id: int):
    gift = Gift.query.get_or_404(gift_id)
    if gift.owner_id != current_user.id:
        flash("You cannot edit this gift", "danger")
        return redirect(url_for("gifts.my_gifts"))
    form = GiftForm(obj=gift)
    if form.validate_on_submit():
        gift.title = form.title.data
        gift.description = form.description.data
        gift.url = form.url.data
        gift.image_url = form.image_url.data
        gift.price = Decimal(str(form.price.data)) if form.price.data is not None else None
        gift.notes = form.notes.data
        if form.image_file.data:
            try:
                gift.image_path = save_upload(form.image_file.data)
            except ValueError as exc:
                flash(str(exc), "danger")
                return render_template("gifts/gift_form.html", form=form, gift=gift)
        db.session.commit()
        flash("Gift updated", "success")
        return redirect(url_for("gifts.my_gifts"))
    return render_template("gifts/gift_form.html", form=form, gift=gift)


@gifts_bp.route("/gifts/<int:gift_id>/delete", methods=["POST"])
@login_required
def delete_gift(gift_id: int):
    gift = Gift.query.get_or_404(gift_id)
    if gift.owner_id != current_user.id:
        flash("You cannot delete this gift", "danger")
        return redirect(url_for("gifts.my_gifts"))
    db.session.delete(gift)
    db.session.commit()
    flash("Gift deleted", "info")
    return redirect(url_for("gifts.my_gifts"))


@gifts_bp.route("/uploads/<path:filename>")
def uploaded_file(filename: str):
    upload_folder = Path(current_app.config["UPLOAD_FOLDER"]).resolve()
    return send_from_directory(upload_folder, filename)


@gifts_bp.route("/images/fetch", methods=["POST"])
@login_required
def image_fetcher():
    data = request.get_json(silent=True) or {}
    url = data.get("url")
    if not url:
        return {"error": "URL required"}, 400
    try:
        path = fetch_image(url)
    except ValueError as exc:
        return {"error": str(exc)}, 400
    return {"path": path}, 200
