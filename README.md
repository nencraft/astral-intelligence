# Astral Intelligence
## Overview

Astral Intelligence is a full-stack astronomy intelligence platform focused on near-Earth objects.

The project ingests NASA NeoWs data, stores normalized object and close-approach records in PostgreSQL, ranks close approaches with a custom C#/.NET scoring
service, and generates AI-assisted technical briefings from verified source data.

## Current Status

Current phase: Phase 2 - NASA NeoWs ingestion

Phase 1 completed:
- PostgreSQL runs through Docker Compose
- Django reads `DATABASE_URL`
- Initial migrations ran against PostgreSQL
- Basic `/api/health/` endpoint works
- `NearEarthObject` and `CloseApproach` models exist
- Models are registered in Django admin
- Read-only API endpoints exist for NEOs and close approaches
- Model and API tests pass
- Manual sample data workflow is documented

## MVP Scope

The MVP focuses on near-Earth objects only.

Core capabilities planned for V1:

- ingest NASA NeoWs data
- store normalized near-Earth object and close-approach records
- expose REST API endpoints through Django REST Framework
- calculate an Astral Priority Score with a C#/.NET service
- save scores in PostgreSQL
- generate structured AI briefings from stored source data
- provide an Angular dashboard and object detail pages
- run locally with Docker
- support a low-cost deployment path with backups

Not included in V1:

- exoplanets
- telescope observation planning
- email alerts
- social features
- payments
- advanced orbital mechanics
- custom machine learning model training

## Tech Stack

### Backend

- Python
- Django
- Django REST Framework
- PostgreSQL
- Docker
- pytest / pytest-django

### Scoring Service

- C#
- ASP.NET Core Web API
- xUnit
- Docker

### Frontend

- Angular
- TypeScript
- RxJS
- Chart.js, ECharts, or similar charting library

### AI

- OpenAI API initially
- Structured briefing generation from stored source data
- No open-ended chatbot behavior in the MVP

### Deployment

Recommended V1 deployment path:

- Frontend: Cloudflare Pages
- Backend/API: AWS Lightsail
- Database: PostgreSQL container on Lightsail
- Scoring service: Dockerized ASP.NET Core service on Lightsail
- Reverse proxy: Caddy or Nginx
- Backups: Lightsail snapshots plus PostgreSQL dumps

## High-Level Architecture

```text
User Browser
    |
    | Angular app
    v
Angular Frontend
    |
    | REST API
    v
Django REST API
    |\
    | \-- fetches data from ----> NASA NeoWs API
    | \-- requests briefings ---> AI Provider API
    | \-- requests scores ------> C#/.NET Scoring Service
    |
    | reads/writes
    v
PostgreSQL Database
```

## Phase 1 Scope

Phase 1 will build the backend foundation.

Planned Phase 1 decisions:

- Django project name: `config`
- First Django app: `neos`
- Use Django REST Framework from the start
- Use PostgreSQL through Docker Compose
- Use real but minimal models:
  - `NearEarthObject`
  - `CloseApproach`
- First endpoint: `GET /api/health/`
- Initial read-only API endpoints:
  - `GET /api/neos/`
  - `GET /api/neos/{id}/`
  - `GET /api/approaches/`
- Use `pytest` and `pytest-django`
- Use `requirements.txt` for Python dependencies
- Keep NASA ingestion out of Phase 1
- Keep C# scoring out of Phase 1
- Keep AI briefings out of Phase 1
- Use Django admin only; no user auth yet

## Environment Variables

Expected future environment variables:

```text
DATABASE_URL
NASA_API_KEY
AI_API_KEY
SCORING_SERVICE_URL
DJANGO_SECRET_KEY
DEBUG
ALLOWED_HOSTS
POSTGRES_PASSWORD
```
Do not commit .env.

## Local Sample Data Workflow

Phase 1 uses manual sample data instead of NASA ingestion.

Start PostgreSQL:

`docker compose up -d db`

From backend/, set the database URL:

`$env:DATABASE_URL="postgres://astral_user:astral_password@localhost:5432/astral_db"`

Run migrations:

`.\.venv\Scripts\python.exe manage.py migrate`

Create a local admin user if needed:

`.\.venv\Scripts\python.exe manage.py createsuperuser`

Run the Django development server:

`.\.venv\Scripts\python.exe manage.py runserver`

Open the admin:

http://127.0.0.1:8000/admin/

Create a sample near-Earth object:
```
nasa_jpl_id: 3542519
name: (2010 PK9)
absolute_magnitude_h: 21.500
estimated_diameter_min_km: 0.120000
estimated_diameter_max_km: 0.270000
is_potentially_hazardous: false
```
Create a sample close approach linked to that object:

close_approach_date: 2026-05-29
epoch_date_close_approach: 1780012800000
relative_velocity_kps: 15.250000
miss_distance_km: 7500000.123
orbiting_body: Earth

Verify the API:

http://127.0.0.1:8000/api/neos/
http://127.0.0.1:8000/api/approaches/

The API should return the sample records as JSON.

## Documentation

Detailed planning docs:

- docs/PROJECT_BRIEF.md
- docs/ROADMAP.md
- docs/ARCHITECTURE.md
- docs/TESTING_PLAN.md
- docs/DEPLOYMENT_NOTES.md

