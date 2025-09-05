# eLearning Platform (Django)

An extensible Django-based eLearning platform supporting courses, chapters, questions, submissions, and media preparation.

## Features (Current)
- User authentication (Django auth)
- Course listing & enrollment (see models in [onlinecourse/models.py](onlinecourse/models.py))
- Question & Choice model structure for exams
- Exam submission and scoring logic (views in [onlinecourse/views.py](onlinecourse/views.py))
- Bootstrap 5 UI base template ([onlinecourse/templates/onlinecourse/base.html](onlinecourse/templates/onlinecourse/base.html))
- Admin interface (Django admin)

## Planned / Roadmap
- Chapter/lesson content model
- Rich media uploads (PDF, video, audio)
- Mock test generation
- Progress tracking & completion metrics
- REST API layer (DRF)
- Certificates and analytics

## Tech Stack
- Python 3.10+
- Django 5.1.x ([elearningPlatform/settings.py](elearningPlatform/settings.py))
- Gunicorn for production ([Procfile](Procfile), [gunicorn.conf.py](gunicorn.conf.py))
- Bootstrap 5 (CDN)
- (Optional) PostgreSQL via psycopg2
- Pillow for image handling

## Project Structure
```
manage.py
elearningPlatform/        # Project settings & WSGI/ASGI
onlinecourse/             # Core app (models, views, templates)
static/                   # Global static assets
    admin/                # (Can be removed — Django provides these)
```

Key files:
- [manage.py](manage.py)
- [elearningPlatform/settings.py](elearningPlatform/settings.py)
- [elearningPlatform/urls.py](elearningPlatform/urls.py)
- [onlinecourse/models.py](onlinecourse/models.py)
- [onlinecourse/views.py](onlinecourse/views.py)
- [onlinecourse/templates/](onlinecourse/templates/)
- [requirements.txt](requirements.txt)

## Requirements
See [requirements.txt](requirements.txt). Core pinned packages:
```
Django, Pillow, gunicorn, jinja2, psycopg2, aiohttp
```

## Quick Start (Development)
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Visit: http://127.0.0.1:8000/

## Environment Variables (.env suggested)
```
SECRET_KEY=change_me
DEBUG=1
ALLOWED_HOSTS=localhost,127.0.0.1
# For PostgreSQL (optional):
# DATABASE_URL=postgres://user:pass@localhost:5432/elearning
```
If using `DATABASE_URL`, integrate with `django-environ` (not yet added).

## Database
Default: SQLite (no extra config).  
Optional: PostgreSQL (install server, set DATABASE_URL, adjust settings loader).

## Running Tests
(Add tests in [onlinecourse/tests.py](onlinecourse/tests.py))
```bash
python manage.py test
```

## Management Commands (Common)
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic
python manage.py shell
```

## Production (Example)
```bash
export DJANGO_SETTINGS_MODULE=elearningPlatform.settings
python manage.py collectstatic --noinput
gunicorn elearningPlatform.wsgi:application --config gunicorn.conf.py
```

Behind NGINX or reverse proxy (enable HTTPS, security headers).

## Static Files
You currently vendor the Django admin under [static/admin](static/admin). Recommended: remove it unless overriding assets; rely on Django’s built-in admin static.

## Security Hardening (To Apply for Production)
- Set `DEBUG=0`
- Add proper `ALLOWED_HOSTS`
- Add `CSRF_COOKIE_SECURE`, `SESSION_COOKIE_SECURE`
- Consider `SECURE_HSTS_SECONDS`
- Use `ManifestStaticFilesStorage`
- Rotate `SECRET_KEY`

## Suggested Next Improvements
1. Split settings into `settings/base.py`, `dev.py`, `prod.py`
2. Add tests for scoring logic (submission evaluation)
3. Add Course slug field for cleaner URLs
4. Introduce DRF for API consumption
5. Pre-commit hooks (black, isort, ruff)
6. CI pipeline (GitHub Actions) for tests & linting

## Example Model Extension (Planned Lesson Model)
```python
class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="lessons")
    title = models.CharField(max_length=180)
    order = models.PositiveIntegerField(default=0)
    body = models.TextField()
```

## License
Add a LICENSE file (e.g., MIT) to clarify reuse.  
Admin icon assets include third‑party licenses (see [static/admin/img/LICENSE](static/admin/img/LICENSE)).

## Contributing
1. Fork
2. Create feature branch
3. Run tests
4. Submit PR

## Contact
Owner: Prince

---
Short goal: stabilize core exam flow, then implement media + API layer.