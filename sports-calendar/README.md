# sports-calendar

Simple MVP for a sports event calendar coding exercise.

## Tech stack
- Python
- FastAPI
- SQLAlchemy
- SQLite

## Project structure

```text
sports-calendar/
├─ app/
├─ docs/
├─ sample_data/
├─ scripts/
└─ tests/
```

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run app

```bash
uvicorn app.main:app --reload
```

Health endpoint:
- `GET /health`

## Import sample events

```bash
python scripts/import_events.py
```

This initializes the database and imports `sample_data/events.json`.

## API endpoints

- `POST /events`
- `GET /events`
- `GET /events/{id}`

### Example: create an event

```bash
curl -X POST "http://127.0.0.1:8000/events" \
  -H "Content-Type: application/json" \
  -d '{
    "season": "2025",
    "status": "scheduled",
    "event_date": "2026-04-01",
    "event_time_utc": "19:30:00",
    "description": "Example derby match",
    "sport_name": "Football",
    "competition_name": "Premier League",
    "stage_name": "Regular Season",
    "stage_ordering": 1,
    "venue_name": "National Stadium",
    "home_team_name": "Team A",
    "away_team_name": "Team B",
    "home_score": 1,
    "away_score": 0,
    "winner": "home"
  }'
```

### Example: list events

```bash
curl "http://127.0.0.1:8000/events"
```

### Example: get one event

```bash
curl "http://127.0.0.1:8000/events/1"
```

## Database file
- Default SQLite file: `sports_calendar.db` (project root)
