# GiftList

## Ubuntu server deployment

Verified on **14 September 2026** against the listeners, user systemd services,
Docker port mappings and deployment registry on `192.168.1.249`.

| Endpoint | Host TCP port | LAN URL |
|---|---:|---|
| Application | 5065 | http://192.168.1.249:5065/ |

Checkout: `/home/zageabb/flask/XmasList`.

These are **user** systemd units. Inspect them with:

```bash
systemctl --user status migrated-flask@XmasList.service
systemctl --user cat migrated-flask@XmasList.service
```

Local verification URL: `http://127.0.0.1:5065/`. HTTP 200 was observed during this audit.

Development defaults and container-internal ports elsewhere in this repository
may differ from this host deployment. Use the live ports above when accessing
this Ubuntu server; do not start a second copy on a port already occupied.

[Complete Ubuntu port inventory](https://github.com/zageabb/universal-deployment-agent/blob/main/UBUNTU_PORTS.md).

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
