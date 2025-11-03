from __future__ import annotations

from urllib.parse import urlparse

from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import DecimalField, StringField, SubmitField, TextAreaField
from wtforms.validators import URL, Length, Optional, ValidationError


def _http_url(_, field):
    if field.data:
        parsed = urlparse(field.data)
        if parsed.scheme not in {"http", "https"}:
            raise ValidationError("URL must start with http or https")


class GiftForm(FlaskForm):
    title = StringField("Title", validators=[Length(min=1, max=255)])
    description = TextAreaField("Description", validators=[Optional(), Length(max=2000)])
    url = StringField("Product URL", validators=[Optional(), URL(require_tld=False), _http_url])
    image_url = StringField("Image URL", validators=[Optional(), URL(require_tld=False), _http_url])
    image_file = FileField(
        "Upload Image",
        validators=[Optional(), FileAllowed({"png", "jpg", "jpeg", "webp"}, "Images only!")],
    )
    price = DecimalField("Price", validators=[Optional()], places=2)
    notes = TextAreaField("Notes", validators=[Optional(), Length(max=2000)])
    submit = SubmitField("Save")
