# Astral Intelligence — Deployment Notes

## Recommended V1 Deployment Target

Use this deployment path for the portfolio/demo version:

- Frontend: Cloudflare Pages
- Backend/API: AWS Lightsail VPS
- Database: PostgreSQL container on the Lightsail VPS
- C# scoring service: Dockerized ASP.NET Core service on the same Lightsail VPS
- Reverse proxy: Caddy or Nginx
- DNS/domain: Cloudflare
- HTTPS: Caddy automatic HTTPS or Cloudflare plus reverse proxy configuration
- Backups: Lightsail snapshots plus PostgreSQL dumps plus off-server copy

## Why This Path

This path is recommended because it is:

- cheap enough for a low-user portfolio project
- simple enough to operate alone
- useful for showing AWS deployment experience
- compatible with Docker Compose
- good for Django, PostgreSQL, and C#/.NET services
- easier than full ECS/RDS/Fargate for V1

Avoid full ECS/RDS/Fargate production architecture for V1 unless there is a specific reason.

## Alternative Deployment Path

Possible alternative:

- Frontend: Cloudflare Pages
- Backend/API: Railway, Render, Fly.io, or similar
- Database: managed PostgreSQL from same provider
- C# scoring service: same provider or Docker-based service

This is acceptable, but the preferred V1 path is Cloudflare Pages plus AWS Lightsail.

---

# Docker and Local Development

Use Docker Compose for:

- Django backend
- PostgreSQL
- C# scoring service
- Redis, optional
- Angular frontend, optional

Suggested services:

- `backend`
- `db`
- `scoring-service`
- `frontend`
- `redis`

## Environment Variables

`.env` should include:

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

Do not commit `.env`.

## PostgreSQL Volume Rule

Do not store database data inside the database container filesystem.

Use a named Docker volume.

Example:

```yaml
services:
  db:
    image: postgres:16
    container_name: astral-postgres
    environment:
      POSTGRES_DB: astral_db
      POSTGRES_USER: astral_user
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

---

# Production Backup Strategy

Use two backup layers:

1. Lightsail automatic snapshots
2. PostgreSQL dump backups

## Layer 1: Lightsail Automatic Snapshots

Enable daily automatic snapshots for the Lightsail instance.

This protects:

- Docker files
- PostgreSQL volume
- uploaded/static files if any
- reverse proxy configuration
- environment and deployment configuration

Use snapshots to recover from whole-server failure.

## Layer 2: Nightly PostgreSQL Dumps

Create nightly compressed PostgreSQL dumps from the database container.

Example backup script:

```bash
#!/usr/bin/env bash
set -euo pipefail

BACKUP_DIR="/opt/astral/backups/postgres"
DATE="$(date +%Y-%m-%d_%H-%M-%S)"
FILE="$BACKUP_DIR/astral_$DATE.sql.gz"

mkdir -p "$BACKUP_DIR"

docker exec astral-postgres pg_dump \
  -U astral_user \
  -d astral_db \
  | gzip > "$FILE"

find "$BACKUP_DIR" -type f -name "*.sql.gz" -mtime +14 -delete
```

This keeps 14 days of local database dumps.

## Off-Server Backup Copy

Backups stored only on the VPS are not enough.

Low-cost options:

- manually download backups to my own computer weekly
- copy encrypted backups to AWS S3
- copy encrypted backups to cloud storage I already use

Simple manual copy example:

```bash
scp ubuntu@your-server:/opt/astral/backups/postgres/latest.sql.gz .
```

For a stronger AWS learning story, use encrypted S3 backup storage.

## Before Risky Changes

Before database migrations or deployment changes, create a manual pre-deploy backup:

```bash
docker compose exec db pg_dump -U astral_user -d astral_db | gzip > pre_deploy_backup.sql.gz
```

Then deploy.

## Restore Testing

At least once per month, verify that a backup can be restored locally.

A backup that has never been restored is only a backup assumption.

---

# Server Maintenance Checklist

## Weekly

Check:

- frontend loads
- Django API health endpoint works
- C# scoring service health endpoint works
- latest PostgreSQL backup exists
- disk space
- Docker container status
- recent logs for obvious errors

Useful commands:

```bash
df -h
docker ps
docker compose ps
ls -lh /opt/astral/backups/postgres | tail
```

## Monthly

Check:

- OS security updates
- whether containers need rebuilds due to base image updates
- one backup restore locally
- AWS bill
- Cloudflare DNS/domain status
- API key usage/costs

---

# AWS Cost Controls

Set AWS budget alerts before deploying.

Suggested alerts:

- `$5 actual`
- `$10 actual`
- `$15 forecasted`
- `$25 actual emergency`

Avoid these for V1 unless needed:

- load balancer
- managed database
- NAT gateway
- multi-instance ECS setup
- always-on large instance
- extra block storage
