from __future__ import annotations

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.exceptions import TooManyRequests

from ..extensions import db
from ..models import User
from ..utils.rate_limit import limit_auth_route
from .forms import LoginForm, PasswordResetRequestForm, RegistrationForm

auth_bp = Blueprint("auth", __name__, template_folder="../templates/auth")


@auth_bp.route("/register", methods=["GET", "POST"])
@limit_auth_route
def register():
    if current_user.is_authenticated:
        return redirect(url_for("gifts.my_gifts"))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data.lower(), name=form.name.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash("Welcome to GiftList!", "success")
        return redirect(url_for("gifts.my_gifts"))
    return render_template("auth/register.html", form=form)


@auth_bp.route("/login", methods=["GET", "POST"])
@limit_auth_route
def login():
    if current_user.is_authenticated:
        return redirect(url_for("gifts.my_gifts"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash("Logged in successfully", "success")
            next_page = request.args.get("next")
            if next_page and next_page.startswith("/"):
                return redirect(next_page)
            return redirect(url_for("gifts.my_gifts"))
        flash("Invalid credentials", "danger")
    return render_template("auth/login.html", form=form)


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out", "info")
    return redirect(url_for("auth.login"))


@auth_bp.route("/password-reset", methods=["GET", "POST"])
@limit_auth_route
def password_reset_request():
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        flash("Password reset functionality is not implemented yet.", "info")
        return redirect(url_for("auth.login"))
    return render_template("auth/password_reset.html", form=form)


@auth_bp.errorhandler(TooManyRequests)
def handle_rate_limit(error: TooManyRequests):
    flash(str(error), "danger")
    return redirect(request.url)
