# Astral Intelligence — Architecture

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

## Recommended Repository Structure

```text
astral-intelligence/
  backend/
  frontend/
  scoring-service/
  docs/
    PROJECT_BRIEF.md
    ROADMAP.md
    ARCHITECTURE.md
    TESTING_PLAN.md
    DEPLOYMENT_NOTES.md
  README.md
  AGENTS.md
  .gitignore
  docker-compose.yml
```

## Service Responsibilities

### Django Backend

Responsible for:

- NASA data ingestion
- PostgreSQL data modeling
- REST API endpoints
- AI briefing generation
- calling the C# scoring service
- persisting scoring results and AI briefings
- sync logging
- authentication later, if needed

Suggested Django apps:

- `neos`
- `scoring`
- `briefings`
- `integrations`
- `accounts` later, not required for V1

### PostgreSQL Database

Stores normalized astronomy and application data.

Core tables:

- `near_earth_objects`
- `close_approaches`
- `astral_scores`
- `ai_briefings`
- `api_sync_runs`

Future V1.5/V2 tables:

- `users`
- `watchlist_items`
- `notification_preferences`

### C#/.NET Scoring Service

A focused microservice that calculates an Astral Priority Score.

Responsibilities:

- accept scoring requests from Django
- validate input
- calculate score
- return category and factor breakdown
- expose health check endpoint
- include xUnit tests
- run in Docker

Endpoints:

```text
GET /health
POST /api/score
```

### Angular Frontend

Displays:

- dashboard
- object search/filtering
- object detail pages
- Astral Priority Score
- AI briefing panel
- saved public/recent briefings
- charts and stats

### AI Briefing Generator

Generates structured briefings from stored, verified data only.

Rules:

- no open-ended chatbot in MVP
- no invented orbital facts
- no invented NASA claims
- no unsupported risk claims
- output should be structured JSON
- every briefing should save the source-data snapshot

---

# Data Model Draft

## NearEarthObject

Fields:

- `id`
- `nasa_jpl_id`
- `name`
- `absolute_magnitude_h`
- `estimated_diameter_min_km`
- `estimated_diameter_max_km`
- `is_potentially_hazardous`
- `first_observed_at`
- `last_synced_at`
- `created_at`
- `updated_at`

## CloseApproach

Fields:

- `id`
- `near_earth_object_id`
- `close_approach_date`
- `epoch_date_close_approach`
- `relative_velocity_kps`
- `miss_distance_km`
- `orbiting_body`
- `created_at`
- `updated_at`

## AstralScore

Fields:

- `id`
- `near_earth_object_id`
- `close_approach_id`
- `score`
- `category`
- `diameter_factor`
- `distance_factor`
- `velocity_factor`
- `timing_factor`
- `hazard_flag_factor`
- `explanation`
- `scored_at`

## AIBriefing

Fields:

- `id`
- `near_earth_object_id`
- `close_approach_id`
- `source_data_snapshot`
- `briefing_type`
- `plain_english_summary`
- `technical_summary`
- `risk_context`
- `data_caveats`
- `model_name`
- `prompt_version`
- `created_at`

## ApiSyncRun

Fields:

- `id`
- `source`
- `started_at`
- `finished_at`
- `status`
- `records_requested`
- `records_created`
- `records_updated`
- `error_message`

## WatchlistItem — V1.5 or V2

Fields:

- `id`
- `user_id`
- `near_earth_object_id`
- `created_at`
- `notes`

---

# Django API Endpoints

Suggested V1 endpoints:

```text
GET /api/neos/
GET /api/neos/{id}/
GET /api/approaches/
GET /api/approaches/upcoming/
POST /api/sync/neows/
POST /api/approaches/{id}/score/
POST /api/approaches/{id}/briefings/
GET /api/briefings/
GET /api/briefings/{id}/
GET /api/health/
```

Suggested V1.5/V2 endpoints:

```text
POST /api/watchlist/
DELETE /api/watchlist/{id}/
GET /api/users/me/
```

## API Filters

For `/api/neos/` and `/api/approaches/`:

- `start_date`
- `end_date`
- `min_score`
- `max_score`
- `hazardous`
- `min_diameter`
- `max_miss_distance`
- `sort_by`

---

# Astral Priority Score

## Purpose

The Astral Priority Score is not an official NASA risk score.

It is a custom portfolio-project score that ranks objects by review priority or interest level.

It should be transparent and explainable.

## Inputs

Potential inputs:

- `estimated_diameter_min_km`
- `estimated_diameter_max_km`
- `miss_distance_km`
- `relative_velocity_kps`
- `is_potentially_hazardous`
- `days_until_close_approach`

## Output Shape

```json
{
  "score": 72,
  "category": "High Interest",
  "factors": {
    "diameter": 20,
    "distance": 24,
    "velocity": 18,
    "timing": 10,
    "hazardFlag": 0
  },
  "explanation": "This object ranks as high interest due to its estimated size, relative velocity, and near-term approach date."
}
```

## Score Categories

```text
0–24: Low Interest
25–49: Moderate Interest
50–74: High Interest
75–100: Critical Review
```

The app must use careful language and must not imply actual danger or official NASA risk.

---

# AI Briefing Design

## Important Rule

The AI must only generate briefings from stored source data.

Do not let the AI invent:

- orbital facts
- impact-risk claims
- NASA claims
- missing measurements
- official classifications not present in the data

## Prompt Requirements

The prompt should include:

- object name
- diameter estimate
- hazardous flag
- close approach date
- relative velocity
- miss distance
- orbiting body
- Astral Priority Score
- explicit instruction not to invent facts
- explicit instruction to mention data caveats

## Output Structure

AI should return structured JSON:

```json
{
  "plainEnglishSummary": "",
  "technicalSummary": "",
  "riskContext": "",
  "dataCaveats": []
}
```

## Saved Source-Data Snapshot

Every AI briefing should save:

- generated briefing text
- exact structured source data used to generate it
- model name
- prompt version
- data caveats
- creation timestamp

This makes the AI feature auditable and helps prevent hallucinated facts.

---

# Frontend Pages

## Dashboard Page

Displays:

- upcoming close approaches
- summary cards
- filters
- priority score distribution
- potentially hazardous count
- closest approach table

## Near-Earth Object Detail Page

Displays:

- object name
- NASA/JPL ID
- diameter estimate
- hazardous flag
- close approach records
- score
- AI briefing button
- saved briefing history

## Briefings Page

Displays:

- saved AI briefings
- date generated
- object name
- score/category
- briefing preview

## Watchlist Page — V1.5 or V2

Displays:

- saved objects
- notes
- upcoming approaches
- score/category

---

# Frontend UI Direction

The UI should be astronomy-related, professional, and not gimmicky.

Suggested style:

- dark background
- indigo accent
- subtle stars
- solid dark cards
- high contrast text
- charts/cards for data
- minimal animations

Avoid:

- cartoon planets
- overly neon sci-fi UI
- too many animations
- NASA clone styling
