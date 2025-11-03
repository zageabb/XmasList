from __future__ import annotations

import mimetypes
import secrets
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin

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


class _ImageMetaParser(HTMLParser):
    CANDIDATE_KEYS = {
        "og:image",
        "og:image:url",
        "og:image:secure_url",
        "twitter:image",
        "twitter:image:src",
        "twitter:image:url",
        "itemprop:image",
    }

    def __init__(self) -> None:
        super().__init__()
        self.image_url: str | None = None

    def handle_starttag(self, tag: str, attrs):  # type: ignore[override]
        if tag.lower() != "meta" or self.image_url:
            return
        attr_map = {name.lower(): value for name, value in attrs if value}
        key = (attr_map.get("property") or attr_map.get("name") or "").lower()
        if key in self.CANDIDATE_KEYS:
            content = attr_map.get("content") or ""
            if content.strip():
                self.image_url = content.strip()


def infer_image_url(page_url: str) -> str | None:
    """Try to infer an image URL from the HTML metadata of ``page_url``."""

    if not page_url:
        return None
    try:
        resp = requests.get(
            page_url,
            timeout=5,
            headers={"User-Agent": "GiftListBot/1.0 (+https://example.com)"},
        )
        resp.raise_for_status()
    except requests.RequestException:
        return None

    content_type = resp.headers.get("Content-Type", "").lower()
    if "html" not in content_type:
        return None

    parser = _ImageMetaParser()
    try:
        parser.feed(resp.text)
        parser.close()
    except Exception:
        return None

    if not parser.image_url:
        return None

    return urljoin(resp.url, parser.image_url)
