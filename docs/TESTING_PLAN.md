# Astral Intelligence — Testing Plan

## Testing Philosophy

Testing is part of the learning goal.

Every major feature should have tests, and I should be able to explain:

- what the test proves
- what edge case it covers
- what bug it would catch
- whether it is a unit, integration, or end-to-end style test

Tests should be added in small increments as features are built.

## Django Backend Tests

Test areas:

- NeoWs API response parsing
- data normalization
- duplicate prevention
- model validation
- API endpoints
- briefing creation with mocked AI response
- scoring service client with mocked C# response
- sync logging

## Django Test Categories

### Model Tests

Potential tests:

- `NearEarthObject` stores required NASA fields correctly
- `CloseApproach` links to a `NearEarthObject`
- `AstralScore` links to object and approach records
- `AIBriefing` stores source-data snapshot
- `ApiSyncRun` records sync status and errors
- constraints prevent duplicate records where appropriate

### Parser and Normalization Tests

Potential tests:

- NeoWs response is parsed into internal data shape
- estimated diameter values are converted correctly
- velocity and miss distance values are stored in expected units
- missing nullable NASA fields are handled safely
- invalid or unexpected payloads fail predictably

### Ingestion Tests

Potential tests:

- first sync creates objects and approaches
- repeated sync updates existing records instead of duplicating them
- failed NASA API calls are logged
- partial failures are handled safely
- sync run records requested, created, updated, and error counts

### API Endpoint Tests

Potential tests:

- list NEOs
- retrieve NEO detail
- list close approaches
- list upcoming close approaches
- filter by date range
- filter by hazardous flag
- filter by minimum score
- trigger score creation
- trigger briefing creation
- list saved briefings
- retrieve briefing detail
- health endpoint returns success

### AI Briefing Tests

AI API calls should be mocked.

Potential tests:

- briefing endpoint uses stored source data only
- prompt includes required source fields
- AI response is parsed as structured data
- briefing is saved with source-data snapshot
- model name and prompt version are stored
- invalid AI response is handled safely

### Scoring Client Tests

C# service calls should be mocked from Django tests.

Potential tests:

- Django sends correct scoring request shape
- successful scoring response is saved
- service timeout is handled
- service error response is logged
- invalid score response is rejected or handled safely

## C# Scoring Service Tests

Use xUnit.

Test areas:

- score calculation
- category mapping
- input validation
- edge cases
- health endpoint

## C# Unit Test Ideas

### Score Calculation

Potential tests:

- larger estimated diameter increases diameter factor
- closer miss distance increases distance factor
- higher relative velocity increases velocity factor
- near-term approach increases timing factor
- hazardous flag affects score if included
- total score remains within 0–100

### Category Mapping

Potential tests:

- 0–24 maps to `Low Interest`
- 25–49 maps to `Moderate Interest`
- 50–74 maps to `High Interest`
- 75–100 maps to `Critical Review`
- boundary values map correctly

### Validation

Potential tests:

- negative diameter is rejected
- negative miss distance is rejected
- negative velocity is rejected
- missing required values are rejected
- impossible values return validation errors

### API Tests

Potential tests:

- `GET /health` returns success
- `POST /api/score` returns score, category, factors, and explanation
- invalid request returns a useful error response

## Angular Frontend Tests

Test areas:

- dashboard rendering
- filter behavior
- API service methods
- loading states
- error states
- object detail page
- briefing generation UI flow

## Angular Test Ideas

### Dashboard

Potential tests:

- dashboard renders summary cards
- close approach table renders API data
- hazardous count displays correctly
- score distribution chart receives expected data

### Filters

Potential tests:

- date filters call API with correct query params
- hazardous filter works
- minimum score filter works
- max miss distance filter works
- sort selection updates displayed results

### Object Detail

Potential tests:

- object detail renders NEO data
- close approaches render under selected object
- score section handles missing score
- briefing button appears when appropriate

### Briefing UI

Potential tests:

- generate briefing button calls API
- loading state displays while request is pending
- generated briefing displays structured sections
- saved briefing history renders
- error state displays when generation fails

## Phase-Based Testing Checkpoints

### Phase 1

Minimum tests:

- health endpoint
- basic model creation
- first simple API endpoint

### Phase 2

Minimum tests:

- NeoWs parser
- ingestion upsert behavior
- sync logging
- API failure handling

### Phase 3

Minimum tests:

- C# score calculation
- C# category boundaries
- C# validation
- Django scoring client with mocked service response

### Phase 4

Minimum tests:

- AI prompt/source-data construction
- mocked AI response parsing
- briefing persistence
- source-data snapshot persistence

### Phase 5

Minimum tests:

- dashboard render
- API service methods
- filter behavior
- object detail render
- briefing UI states

### Phase 6

Minimum checks:

- production health endpoints
- Docker Compose services start
- backup script works
- one backup can be restored locally
- deployment instructions are accurate
