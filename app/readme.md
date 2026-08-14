# Scalable URL Shortener

A production-oriented URL shortening service built with Python and FastAPI,
designed with caching, rate limiting, load balancing, database persistence,
and application observability.

## Features

- Create short URLs using Base62 encoding
- Redirect short URLs to original URLs
- PostgreSQL for persistent storage
- Redis for caching
- Redis-based rate limiting
- Nginx reverse proxy and load balancing
- Prometheus metrics
- Grafana monitoring
- Centralized application logging
- Docker Compose based deployment
- Health checks

## Architecture

```
                Client
                  |
                Nginx
           /      │       \
    FastAPI    FastAPI     FastAPI
  Instance 1  Instance 2  Instance 3
                  │              
                Redis
        Cache / Rate Limiting
                  │
             PostgreSQL
              Database

  Prometheus - Grafana
```

Prometheus → Grafana
Application → Logs

## Tech Stack

| Category | Technology |
|---|---|
| Language | Python |
| Framework | FastAPI |
| Database | PostgreSQL |
| Cache | Redis |
| Reverse Proxy | Nginx |
| Monitoring | Prometheus, Grafana |
| Containerization | Docker, Docker Compose |
| API | REST |
| Version Control | Git |

## Key Decisions

### Base62 URL generation

Short URLs are generated using Base62 encoding to create compact
URL identifiers.

### Redis caching

Frequently accessed URLs are cached in Redis to reduce database
queries and improve redirect performance.

### Rate limiting

Redis is used to implement request rate limiting and protect the
service from excessive traffic.

### PostgreSQL

PostgreSQL provides durable storage for URL mappings and supports
reliable transactional operations.

### Nginx load balancing

Nginx distributes incoming requests across multiple FastAPI
instances, allowing the application layer to scale horizontally.

### Observability

Prometheus collects application and infrastructure metrics while
Grafana provides dashboards for monitoring system health.

## To Run Locally

### Prerequisites

- Docker
- Docker Compose

### Start the application

```bash
docker compose up --build
