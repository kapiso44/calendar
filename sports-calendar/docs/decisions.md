# Technical decisions

## Stack
- **FastAPI** for the app skeleton and future endpoints.
- **SQLAlchemy + SQLite** for a lightweight relational data layer.

## Schema decisions
- Reference data (teams, competitions, stages, venues) is normalized to avoid duplicate strings.
- Event foreign keys use underscore-prefixed names (for example `_sport_id`) per project constraint.
- Most foreign keys are nullable to support partially-populated source payloads.

## Import decisions
- A default `Football` sport is always created/fetched.
- Team deduplication follows a practical order: external ID, then slug, then name.
- Original source payload is stored in `events.source_payload_json` for debugging.
