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

Current Phase 2 ingestion services inside `neos`:

```text
neos/services/neows_client.py
neos/services/neows_normalizer.py
neos/services/neows_upsert.py
neos/services/sync_logger.py
neos/management/commands/sync_neows.py
```
Responsibilities:

- `neows_client.py`: calls NASA NeoWs Feed and handles HTTP/client errors
- `neows_normalizer.py`: converts NASA response data into internal Python data
- `neows_upsert.py`: creates or updates NEOs and close approaches without duplicates
- `sync_logger.py`: records sync lifecycle and result counts
- `sync_neows.py`: orchestrates the services through a management command

Suggested Django apps:

- neos
- scoring
- briefings
- integrations
- accounts (later)

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

- Use Django internal IDs as primary keys.
- Use `nasa_jpl_id` as the unique NASA/JPL identifier for near-Earth objects.

## NearEarthObject

Current fields:

- `id`
- `nasa_jpl_id`
- `name`
- `absolute_magnitude_h`
- `estimated_diameter_min_km`
- `estimated_diameter_max_km`
- `is_potentially_hazardous`
- `last_synced_at`
- `created_at`
- `updated_at`

Possible future fields:

- `first_observed_at`

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

Duplicate prevention:

- `near_earth_object_id`
- `epoch_date_close_approach`
- `orbiting_body`

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
- `status`
- `start_date`
- `end_date`
- `started_at`
- `finished_at`
- `records_requested`
- `records_created`
- `records_updated`
- `records_skipped`
- `error_message`

Purpose:

- records every NASA NeoWs sync attempt
- stores requested date range
- tracks success or failure
- stores created, updated, and skipped counts
- preserves error messages for failed syncs

---

# Django API Endpoints

Current backend endpoints:

```text
GET /api/health/
GET /api/neos/
GET /api/neos/{id}/
GET /api/approaches/
GET /api/approaches/{id}/
```

Current ingestion command:

`python manage.py sync_neows --start-date YYYY-MM-DD --end-date YYYY-MM-DD`

Suggested future V1 endpoints:

```text
GET /api/approaches/upcoming/
POST /api/sync/neows/
POST /api/approaches/{id}/score/
POST /api/approaches/{id}/briefings/
GET /api/briefings/
GET /api/briefings/{id}/
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

It is a custom portfolio-project score that ranks near-Earth object close approaches by review priority and
interest level.

It should be transparent, deterministic, and explainable.

The score must not be described as a collision probability, danger rating, or official impact-risk
assessment.

## Model Version

The initial scoring model is:

```text
APS-v1
```

Scores should include the model version that produced them.

This keeps scores explainable if the scoring formula changes later.

Future scoring changes should use a new version, such as `APS-v2`.

## Calibration Sample

APS-v1 uses fixed thresholds calibrated from a controlled NASA NeoWs Feed sample.

Sample window:

```text
2026-01-08 through 2026-07-07
```

Sample size:

```text
847 close approaches
```

The thresholds are not recalculated during normal ingestion or scoring.

They may be reviewed periodically, such as yearly, after enough additional NASA data has been collected to
justify a scoring-model update.

## Inputs

The scoring service should accept one close approach at a time.

Input fields:

- `estimatedDiameterMinKm`
- `estimatedDiameterMaxKm`
- `missDistanceKm`
- `relativeVelocityKps`
- `isPotentiallyHazardous`
- `closeApproachDate`

The diameter factor should use the average of the minimum and maximum estimated diameter:

```text
averageDiameterKm = (estimatedDiameterMinKm + estimatedDiameterMaxKm) / 2
```

## Score Factors

The total score is 0-100 points.

```text
diameter factor + distance factor + velocity factor + timing factor + hazard flag factor
```

Factor weights:

```text
diameter: 0-25
distance: 0-25
velocity: 0-20
timing: 0-15
hazard flag: 0-15
```

## APS-v1 Thresholds

### Diameter Factor

```text
averageDiameterKm < 0.03 = 2
0.03 to < 0.065 = 8
0.065 to < 0.20 = 15
0.20 to < 0.60 = 21
>= 0.60 = 25
```

### Distance Factor

Closer approaches receive more points.

```text
missDistanceKm > 57,000,000 = 2
37,000,000 to 57,000,000 = 8
20,000,000 to < 37,000,000 = 15
1,000,000 to < 20,000,000 = 21
< 1,000,000 = 25
```

### Velocity Factor

```text
relativeVelocityKps < 8 = 2
8 to < 13 = 6
13 to < 18 = 12
18 to < 27 = 16
>= 27 = 20
```

### Timing Factor

The timing factor is based on how soon the close approach occurs.

Past close approaches are still scoreable, but receive 0 timing points.

```text
past approach = 0
> 365 days away = 1
90 to 365 days away = 5
30 to < 90 days away = 9
7 to < 30 days away = 12
0 to < 7 days away = 15
```

### Hazard Flag Factor

```text
isPotentiallyHazardous = false = 0
isPotentiallyHazardous = true = 15
```
## Score Categories

```text
0-24: Low Interest
25-49: Moderate Interest
50-74: High Interest
75-100: Critical Review
```

## Output Shape

```json
{
  "score": 63,
  "category": "High Interest",
  "modelVersion": "APS-v1",
  "factors": {
    "diameter": 21,
    "distance": 21,
    "velocity": 12,
    "timing": 9,
    "hazardFlag": 0
  },
  "explanation": "High interest due to size, miss distance, and relative velocity."
}
```

The explanation should describe why the close approach received its score without implying actual danger or
official NASA risk.

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
