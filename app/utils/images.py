from __future__ import annotations

import mimetypes
import secrets
from pathlib import Path

import requests
from flask import current_app
from PIL import Image
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

ALLOWED_MIME_TYPES = {"image/png", "image/jpeg", "image/webp"}


def _safe_filename(filename: str) -> str:
    base = secure_filename(filename)
    if not base:
        base = secrets.token_hex(8)
    return base


def _upload_folder() -> Path:
    folder = Path(current_app.config["UPLOAD_FOLDER"])
    folder.mkdir(parents=True, exist_ok=True)
    return folder


def save_upload(file: FileStorage) -> str:
    upload_folder = _upload_folder()
    filename = _safe_filename(file.filename or "upload")
    extension = Path(filename).suffix or ".jpg"
    filepath = upload_folder / f"{secrets.token_hex(8)}{extension}"
    file.stream.seek(0)
    file.save(filepath)
    _validate_image(filepath)
    return filepath.name


def fetch_image(url: str) -> str:
    resp = requests.get(url, timeout=5)
    resp.raise_for_status()
    content_type = resp.headers.get("Content-Type", "").split(";")[0]
    if content_type not in ALLOWED_MIME_TYPES:
        raise ValueError("Unsupported image type")
    extension = mimetypes.guess_extension(content_type) or ".jpg"
    upload_folder = _upload_folder()
    filename = upload_folder / f"{secrets.token_hex(8)}{extension}"
    with open(filename, "wb") as f:
        f.write(resp.content)
    _validate_image(filename)
    return filename.name


def _validate_image(path: Path) -> None:
    max_size = current_app.config.get("MAX_CONTENT_LENGTH", 2 * 1024 * 1024)
    if path.stat().st_size > max_size:
        path.unlink(missing_ok=True)
        raise ValueError("Image file is too large")
    try:
        with Image.open(path) as image:
            image.verify()
    except Exception as exc:  # pragma: no cover - safety net
        path.unlink(missing_ok=True)
        raise ValueError("Invalid image file") from exc
