# Astral Intelligence — Roadmap

# Development Standards

- Keep changes small and explainable
- Add tests with each major feature
- Prefer clear names over clever abstractions
- Do not add services before their roadmap phase
- Use environment variables for secrets
- Do not commit `.env`

# Phase 0: Project Setup and Planning

## Deliverables

- GitHub repo
- `docs/PROJECT_BRIEF.md`
- `docs/ROADMAP.md`
- `docs/ARCHITECTURE.md`
- `AGENTS.md`
- `docs/TESTING_PLAN.md`
- `docs/DEPLOYMENT_NOTES.md`
- `README.md`
- `.gitignore`

## Definition of Done

- Project documentation exists
- Initial architecture and roadmap are documented
- Development standards are defined
- Phase 1 implementation scope is clear

---

# Phase 1: Backend Foundation

## Phase 1A: Backend Foundation Setup - Complete

Completed:
- Django project created in `backend/`
- Django project name: `config`
- Django app created: `neos`
- Django REST Framework installed
- PostgreSQL configured through Docker Compose
- Django configured to use `DATABASE_URL`
- Initial migrations ran against PostgreSQL
- `/api/health/` endpoint works

## Phase 1B: NEO Domain Models - Complete

Goal:
- Design and implement the first minimal NEO data model.

Planned:
- `NearEarthObject`
- `CloseApproach`
- model constraints
- migrations
- admin registration
- basic model tests

Completed:
- `NearEarthObject` model
- `CloseApproach` model
- `nasa_jpl_id` unique constraint
- model migration
- Django admin registration
- model tests

## Phase 1C: Read-Only API - Complete

Completed:
- serializers for NEOs and close approaches
- read-only DRF viewsets
- app-level API routing
- list/detail endpoints for NEOs
- list/detail endpoints for close approaches
- API tests

## Phase 1D: Admin and Sample Data Workflow - Complete

Completed:
- Django admin workflow verified
- manual sample NEO can be created
- manual close approach can be linked to a NEO
- API returns manually created sample records
- README documents local sample data workflow

## Phase 1E: Cleanup and Documentation - Complete

Completed:
- Phase 1 documentation updated
- final Django checks passed
- model and API tests passed

## Phase 1 Scope Decisions

- Django project name: `config`
- First Django app: `neos`
- Use Django REST Framework from the start
- Use PostgreSQL through Docker Compose
- Use real but minimal NEO models:
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
- Keep C# scoring service out of Phase 1
- Keep AI briefings out of Phase 1
- Use Django admin only; no user auth yet

## Deliverables

- Django project
- PostgreSQL
- Docker Compose
- Basic models (minimal drafts)
- Basic REST endpoints
- Admin panel
- Initial tests

## Definition of Done

- Django runs locally
- PostgreSQL runs through Docker Compose
- Initial models migrate successfully
- Admin panel works
- A basic health endpoint works
- Initial tests pass
- README has local setup steps
- Read-only NEO API endpoints work
- Model and API tests pass
- Manual sample data workflow is documented

---

# Phase 2: NASA Ingestion - Complete

## Completed

- NeoWs Feed API client using `httpx`
- `sync_neows` Django management command
- NeoWs response normalization
- Database upsert service
- Duplicate prevention for close approaches
- Sync logging through `ApiSyncRun`
- Tests for client behavior, normalization, upserts, sync logging, and command orchestration

## Definition of Done

- Can run a command to pull NASA NeoWs Feed data
- Objects and close approaches are stored cleanly
- Repeated sync does not create duplicates
- API failures are logged
- Tests cover parsing, upserts, duplicate prevention, and failure handling

---

# Phase 3 - C# Scoring Service

## Deliverables

- ASP.NET Core API
- Score endpoint
- Health endpoint
- Unit tests
- Dockerfile
- Django integration

## Definition of Done

- C# service runs locally
- `POST /api/score` returns score, category, and factor breakdown
- `GET /health` works
- xUnit tests cover score and category behavior
- Django can call scoring service and save result

---

# Phase 4: AI Briefings

## Deliverables

- Structured briefing endpoint
- Prompt template
- Saved briefings
- Source-data snapshot
- Mocked tests

## Definition of Done

- Briefing endpoint uses stored data only
- AI output is structured
- Briefing is saved with source-data snapshot
- Prompt has clear no-hallucination instructions
- Tests mock the AI API

---

# Phase 5: Angular Frontend

## Deliverables

- Dashboard
- Filters
- Object detail page
- API services
- Loading states
- Error states
- Briefing UI

## Definition of Done

- User can view upcoming approaches
- User can filter and search objects
- User can open object details
- User can generate and view a briefing
- Frontend handles loading and error states

---

# Phase 6: Deployment and Operations

## Deliverables

- Cloudflare Pages frontend deployment
- AWS Lightsail backend deployment
- Docker Compose production setup
- PostgreSQL container with named volume
- Caddy or Nginx reverse proxy
- HTTPS and domain configuration
- Lightsail automatic snapshots
- Nightly PostgreSQL dump backups
- Backup restore instructions
- README deployment guide
- Architecture diagram
- Demo screenshots or video
- Tests passing

## Definition of Done

- Public frontend URL works
- Public/proxied backend API works
- Django can connect to PostgreSQL
- Django can call C# scoring service
- AI briefing generation works
- Backups are configured
- One backup restore has been tested locally
- README explains deployment and backup strategy

---

# Version 1.5: Product Depth

Possible additions:

- user accounts
- private saved briefings
- personal watchlists
- OpenAPI/Swagger docs
- GitHub Actions CI
- better deployment logging
- basic admin dashboard

---

# Version 2: Expansion

Possible additions:

- email alerts
- advanced analytics
- Exoplanet Atlas module
- observation planner
- AI cost controls
- expanded C# scoring service
- scoring versioning
