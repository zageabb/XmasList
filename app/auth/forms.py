from __future__ import annotations

from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError

from ..models import User


class RegistrationForm(FlaskForm):
    name = StringField("Name", validators=[Length(min=2, max=120)])
    email = StringField("Email", validators=[Email(), Length(max=255)])
    password = PasswordField("Password", validators=[Length(min=6)])
    confirm = PasswordField("Confirm Password", validators=[EqualTo("password")])
    submit = SubmitField("Register")

    def validate_email(self, field: StringField) -> None:
        if User.query.filter_by(email=field.data.lower()).first():
            raise ValidationError("Email already registered.")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[Email(), Length(max=255)])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")


class PasswordResetRequestForm(FlaskForm):
    email = StringField("Email", validators=[Email(), Length(max=255)])
    submit = SubmitField("Request Password Reset")


class PasswordResetForm(FlaskForm):
    password = PasswordField("New Password", validators=[Length(min=6)])
    confirm = PasswordField("Confirm Password", validators=[EqualTo("password")])
    submit = SubmitField("Reset Password")
