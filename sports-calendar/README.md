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

## Database file
- Default SQLite file: `sports_calendar.db` (project root)
