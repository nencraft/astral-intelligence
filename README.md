# Astral Intelligence

AI-assisted near-Earth object monitoring and briefing platform.

## Overview

Astral Intelligence is a full-stack astronomy intelligence platform focused on near-Earth objects.

The project ingests NASA NeoWs data, stores normalized object and close-approach records in PostgreSQL, ranks close approaches with a custom C#/.NET scoring
service, and generates AI-assisted technical briefings from verified source data.

## Current Status

Current phase: Phase 1B - NEO domain model planning and implementation

Completed:
- Phase 0 project planning
- Phase 1A Django backend foundation
- PostgreSQL Docker Compose setup
- DATABASE_URL-based Django database configuration
- Initial Django migrations
- Basic `/api/health/` endpoint

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

## Documentation

Detailed planning docs:

- docs/PROJECT_BRIEF.md
- docs/ROADMAP.md
- docs/ARCHITECTURE.md
- docs/TESTING_PLAN.md
- docs/DEPLOYMENT_NOTES.md

AI working rules:

- AGENTS.md

## Project Goal

The goal is to build an interview-explainable full-stack software project.

The finished project should clearly demonstrate:

- Django backend development
- PostgreSQL schema design
- NASA API ingestion and normalization
- REST API design
- C#/.NET microservice communication
- AI output grounded in source data
- Angular frontend development
- Dockerized development
- testing strategy
- low-cost cloud deployment and backups
