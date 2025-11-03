# GiftList

GiftList is a multi-user Christmas gift planning web application built with Flask. It allows families and friends to share wish lists, mark gifts as purchased, and keep surprises intact.

## Features

- User authentication with registration, login, logout, and CSRF protection.
- Gift CRUD with optional image uploads or remote image fetching.
- Purchasing workflow that respects privacy (owners never see purchased status on their own items).
- "Purchased by Me" summary view.
- Searchable user directory to browse public gift lists.
- SQLite for local development and PostgreSQL-ready configuration for production.
- Alembic migrations, pytest suite, and seed command for demo data.

## Getting Started

### Prerequisites

- Python 3.11+
- pip

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows use .venv\\Scripts\\activate
pip install -r requirements.txt
cp .env.example .env
flask db upgrade
flask seed
flask run
```

By default the app uses SQLite. To use PostgreSQL, set `DATABASE_URL` in `.env` to a valid connection string.

### Environment Variables

| Variable | Description |
| --- | --- |
| `FLASK_ENV` | Application environment (`development`, `production`, `testing`). |
| `SECRET_KEY` | Secret key used for session signing. |
| `DATABASE_URL` | Database connection string. |
| `UPLOAD_FOLDER` | Directory for uploaded images. |
| `MAX_CONTENT_LENGTH` | Max upload size in bytes. |

## Running Tests

```bash
pytest
```

## Project Structure

```
app/
  auth/          # Authentication blueprint
  gifts/         # Gift management blueprint
  purchases/     # Purchase workflow blueprint
  users/         # User directory and public list views
  templates/     # Jinja templates with Bootstrap styling
  static/        # CSS and images
migrations/      # Alembic migrations
tests/           # Pytest test suite
```

## Deployment

The repository includes a `Procfile` for deploying with Gunicorn and a `runtime.txt` to pin the Python version. Configure environment variables accordingly.

## License

MIT
