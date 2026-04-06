# FitQuest

![Build](https://img.shields.io/badge/build-unknown-lightgrey?style=flat-square)
![Tests](https://img.shields.io/badge/tests-unknown-lightgrey?style=flat-square)
![Coverage](https://img.shields.io/badge/coverage-unknown-lightgrey?style=flat-square)
![License](https://img.shields.io/badge/license-TBD-lightgrey?style=flat-square)

**FitQuest** is a gamified fitness platform where challenges, achievements, and real‑time leaderboards turn workouts into social, measurable progress.

---

## Key Features

- **Challenge system**: Create multi‑day challenges with difficulty tiers, start dates, and scoring rules.
- **Progress logging**: Log reps or minutes daily with automatic totals.
- **Achievements**: Milestone badges and score‑based unlocks.
- **Live leaderboards**: Rankings recalculate on every log.
- **Notifications**: In‑app alerts for wins, milestones, and updates.
- **Admin toggle**: Enable or disable start/end notifications per challenge.
- **API ready**: REST + async endpoints for integrations.

---

## Tech Stack

- **Backend**: Django, Django REST Framework
- **Auth**: JWT via SimpleJWT
- **Async/Jobs**: Celery
- **Broker/Cache**: Redis
- **Static**: WhiteNoise
- **Database**: PostgreSQL (recommended), SQLite for local dev

---

## Installation & Setup

```bash
pip install -r requirements.txt
```

```bash
Create a `.env` file with values for:
DB_NAME=fitquest_db
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=127.0.0.1
DB_PORT=5432
SECRET_KEY=django-insecure-g_^4__q8jp+9fsr)*r%9a0q5&34hvxf*=#jwgy3tqm4_&4)w13
DEBUG=True
CSRF_TRUSTED_ORIGINS=http://127.0.0.1,http://localhost
ALLOWED_HOSTS=127.0.0.1,localhost
```

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

---

## Architecture

Apps and responsibilities:

- `challenges` — challenge lifecycle, ownership rules, schedule validation, notification toggle
- `contestants` — join/leave helpers, progress logging, auto leaderboard refresh
- `achievements` — milestone and score‑based badge unlocking
- `leaderboard` — rank calculation, totals, public + template views
- `notifications` — unread count + activity alerts
- `api` — DRF endpoints, serializers, JWT auth

---

## Testing

```bash
python manage.py test
```

---

## Deployment

- Static files via WhiteNoise (`STATIC_ROOT/staticfiles`).
- Celery uses Redis by default (`redis://localhost:6379/0`).
- Configure `DATABASES`, `SECRET_KEY`, JWT lifetimes, and `ALLOWED_HOSTS` via environment variables.
- Run Celery beat to schedule start/end notifications; disable per challenge with `notify_start_end` in admin.

---

## Security Features

- **JWT authentication** with short‑lived access tokens and refresh tokens.
- **Session protection** via Django middleware and CSRF safeguards.
- **Environment‑based secrets** for `SECRET_KEY`, database credentials, and JWT settings.
- **Per‑object ownership rules** enforced in challenge update/delete flows.
- **Admin toggle** to disable start/end notifications per challenge when needed.

---

## Future Improvements

1. Streak‑aware scoring and streak‑based achievements.
2. Challenge analytics (pacing, averages, personal bests).
3. API filtering, pagination, and activity feeds.
4. Web or mobile client for richer UI.

---

## License

Simeon Hristov
