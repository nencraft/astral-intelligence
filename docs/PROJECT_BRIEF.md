# Astral Intelligence — Project Brief

## Project Name

Astral Intelligence

## Subtitle

AI-assisted near-Earth object monitoring and briefing platform

## One-Sentence Concept

Astral Intelligence is a full-stack astronomy intelligence platform that ingests NASA near-Earth object data, stores and analyzes it in PostgreSQL, calculates an Astral Priority Score with a C#/.NET service, and generates AI-assisted technical briefings from verified source data.

## Elevator Pitch

Astral Intelligence helps users monitor, rank, and understand near-Earth objects using real NASA data.

The app combines a Python/Django backend, PostgreSQL database, Angular/TypeScript frontend, C#/.NET scoring microservice, AI-generated briefings, Dockerized local development, and a low-cost cloud deployment.

The goal is not to build a simple NASA API dashboard. The goal is to build a serious software engineering portfolio project that demonstrates backend development, API integration, relational modeling, AI integration, full-stack UI work, testing, microservice communication, deployment, and basic production operations.

## Product Identity

Astral Intelligence should be presented as:

> An AI-assisted astronomy intelligence platform for monitoring, scoring, and explaining near-Earth objects using NASA data.

It should not be presented as:

> A NASA API dashboard.

The project should feel like an intelligence tool, not a simple data viewer.

## Core Data Source

The MVP uses NASA NeoWs as the core data source.

NeoWs provides near-Earth asteroid information, including:

- searching asteroids by closest approach date
- looking up asteroids by NASA/JPL small-body ID
- browsing the near-Earth object dataset

Optional future data sources may include NASA APOD or NASA Exoplanet Archive, but they are not part of the MVP.

## Engineering Goals

This project demonstrates:

- backend API development with Django and Django REST Framework
- relational data modeling with PostgreSQL
- NASA API ingestion and normalization
- microservice communication with an ASP.NET Core scoring service
- structured AI-assisted briefing generation from verified source data
- frontend development with Angular and TypeScript
- Dockerized local development
- cloud deployment planning
- testing and operational documentation

## Technical Positioning

The project supports this career direction:

- Python primary
- C#/.NET secondary
- PostgreSQL/SQL visible and meaningful
- TypeScript/Angular for full-stack capability
- AWS for deployment credibility
- AI as a practical feature, not a gimmick

C++ is not part of this project.

## Main Portfolio Claim

Astral Intelligence is a serious full-stack software engineering project that combines backend data ingestion, relational modeling, AI-assisted explanation, microservice architecture, cloud deployment, and basic production operations around a real astronomy data source.

## MVP Scope Summary

The MVP focuses on near-Earth objects only.

Core MVP capabilities:

- ingest NASA NeoWs data
- store normalized near-Earth object and close-approach records
- expose REST API endpoints through Django
- calculate custom Astral Priority Scores through a C#/.NET service
- save scores in PostgreSQL
- generate structured AI briefings from stored verified data
- save briefing history and source-data snapshots
- provide an Angular dashboard and object detail pages
- run locally through Docker
- support a low-cost deployment path with backups

## Not in MVP

The following are intentionally excluded from version 1:

- exoplanets
- telescope observation planner
- email alerts
- complex authentication
- social sharing
- payments
- advanced orbital mechanics
- real-time simulation
- custom machine learning model training

These can move to V1.5 or V2 after the NEO-focused platform works.

## Success Criteria

The project is successful only if I can explain:

- the architecture without notes
- how the Django backend works
- how PostgreSQL models and relationships are designed
- how NASA ingestion handles duplicates and failures
- how the C# scoring service calculates scores
- how AI briefings are grounded in source data
- how to run and explain the tests
- how the app is deployed and backed up
- tradeoffs and future improvements in an interview\

## AI Safety and Grounding

AI briefings must be generated only from stored, verified source data.

Briefings should include:

- plain English summary
- technical summary
- risk context
- data caveats

Every briefing should save:

- generated text
- exact source-data snapshot
- model name
- prompt version
- creation timestamp

The AI must not invent orbital facts, NASA claims, or unsupported risk claims.
