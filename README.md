# Django Advanced Blog

A blog backend built with Django and Django REST Framework. It includes email-based authentication with account verification, a REST API for posts and categories, and a fully containerized development setup with CI.

## Features

- **Custom user model** with email login and an automatically created profile
- **Registration with email verification:** signed activation link that expires after 24 hours, plus a rate-limited endpoint to resend it
- **Authentication:** JWT, token and session authentication, change-password and profile endpoints
- **Custom permissions:** only verified users can use protected account endpoints, only a post's author can edit or delete it, only staff can manage categories
- **Posts and categories REST API** with filtering, search, ordering and pagination; drafts are visible only to their author
- **API documentation** with Swagger UI and ReDoc
- **Tests** written with pytest and Django's test framework
- **CI** with GitHub Actions (flake8 + pytest) and Dependabot

## Tech Stack

Python, Django 6, Django REST Framework, Simple JWT, django-filter, drf-yasg, Redis and Celery (worker configured), Docker / Docker Compose, pytest, flake8, black, GitHub Actions

## Getting Started

Requirements: Docker and Docker Compose.

```bash
git clone https://github.com/masih86/django-advanced-blog.git
cd django-advanced-blog
cp .env.example .env        # then set a real SECRET_KEY
docker compose up --build
```

In another terminal, apply migrations and create an admin user:

```bash
docker compose exec backend python manage.py migrate
docker compose exec backend python manage.py createsuperuser
```

| Service | URL |
|---|---|
| API / app | http://localhost:8000 |
| Swagger UI | http://localhost:8000/swagger/ |
| ReDoc | http://localhost:8000/redoc/ |
| Admin | http://localhost:8000/admin/ |
| smtp4dev (inspect sent emails) | http://localhost:5000 |

Activation emails are not sent to real inboxes in development: open smtp4dev to read them and copy the activation link.

### Environment variables

Configured in `.env` (see `.env.example`):

| Variable | Description | Default |
|---|---|---|
| `SECRET_KEY` | Django secret key (required) | none |
| `DEBUG` | Debug mode | `False` |
| `ALLOWED_HOSTS` | Comma-separated list of hosts | `localhost,127.0.0.1` |
| `EMAIL_HOST` | SMTP host | `smtp4dev` |
| `EMAIL_PORT` | SMTP port | `25` |
| `DEFAULT_FROM_EMAIL` | Sender address | `noreply@example.com` |
| `CELERY_BROKER_URL` | Celery broker | `redis://redis:6379/1` |
| `CELERY_RESULT_BACKEND` | Celery result backend | `redis://redis:6379/1` |

## API Overview

### Accounts (`/accounts/api/v1/`)

| Method | Endpoint | Description |
|---|---|---|
| POST | `registration/` | Create an account and send an activation email |
| GET | `activation/confirm/<token>/` | Verify the account |
| POST | `activation/resend/` | Resend the activation email (limited to 5 requests/hour) |
| POST | `jwt/create/` | Obtain a JWT access/refresh pair |
| POST | `jwt/refresh/` | Refresh an access token |
| POST | `jwt/verify/` | Verify a token |
| POST | `token/login/` | Obtain an auth token |
| POST | `token/logout/` | Delete the auth token (token authentication only) |
| PUT | `change-password/` | Change the current user's password |
| GET, PUT, PATCH | `profile/` | Retrieve or update the current user's profile |

### Blog (`/blog/api/v1/`)

| Method | Endpoint | Description |
|---|---|---|
| GET, POST | `post/` | List published posts / create a post (authentication required) |
| GET, PUT, PATCH, DELETE | `post/<id>/` | Retrieve a post / modify it (author only) |
| GET, POST | `category/` | List categories / create one (staff only) |
| GET, PUT, PATCH, DELETE | `category/<id>/` | Retrieve a category / modify it (staff only) |

Post list query parameters: `?category=`, `?author=`, `?search=`, `?ordering=` (`created_date`, `published_date`), `?page=`, `?page_size=`

## Running Tests

```bash
docker compose exec backend pytest
docker compose exec backend flake8
```

## Project Structure

```
accounts/   custom user, profile, registration, verification, auth endpoints
blog/       posts and categories (HTML views and REST API)
core/       project settings, URLs, Celery configuration
```

## Known Limitations

Decisions I made knowingly for this project, and what I would change next:

- **Activation emails are sent in a background thread** instead of a task queue. A Celery task with retries would be more reliable if the server restarts mid-send. The Celery worker and Redis are already configured in Docker Compose, but no tasks are defined yet.
- **SQLite** is used for development; PostgreSQL would be the choice for production.
- **Several authentication methods** (JWT, token, session) are enabled because the project was built as a learning exercise. A production API would standardize on one, most likely JWT.
- **Logout** (`token/logout/`) only works for token authentication; JWT users should simply discard their tokens client-side.

## License

This project was created for educational purposes.