import json
import sys
from collections.abc import Iterable
from datetime import date
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import SessionLocal, init_db
from app.models import Competition, Event, EventResult, Sport, Stage, Team, Venue


def safe_parse_date(value: str | None) -> date | None:
    if not value:
        return None
    try:
        return date.fromisoformat(value)
    except ValueError:
        return None


def load_events_json(path: Path) -> list[dict]:
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    if isinstance(data, list):
        return data
    if isinstance(data, dict) and isinstance(data.get("events"), list):
        return data["events"]
    raise ValueError("JSON must be a list of events or an object with an 'events' list")


def get_or_create_sport(db: Session, name: str = "Football") -> Sport:
    sport = db.scalar(select(Sport).where(Sport.name == name))
    if sport:
        return sport

    sport = Sport(name=name)
    db.add(sport)
    db.flush()
    return sport


def get_or_create_competition(db: Session, item: dict, counters: dict[str, int]) -> Competition | None:
    external_id = item.get("originCompetitionId")
    name = item.get("originCompetitionName")

    if external_id is None and not name:
        return None

    competition = None
    if external_id is not None:
        competition = db.scalar(select(Competition).where(Competition.external_id == external_id))

    if not competition and name:
        competition = db.scalar(select(Competition).where(Competition.name == name))

    if competition:
        return competition

    competition = Competition(external_id=external_id, name=name or "Unknown Competition")
    db.add(competition)
    db.flush()
    counters["competitions"] += 1
    return competition


def get_or_create_stage(db: Session, stage_data: dict | None, counters: dict[str, int]) -> Stage | None:
    if not stage_data:
        return None

    external_id = stage_data.get("id")
    name = stage_data.get("name") or "Unknown Stage"
    ordering = stage_data.get("ordering")

    stage = None
    if external_id is not None:
        stage = db.scalar(select(Stage).where(Stage.external_id == external_id))

    if not stage:
        stage = db.scalar(select(Stage).where(Stage.name == name, Stage.ordering == ordering))

    if stage:
        return stage

    stage = Stage(external_id=external_id, name=name, ordering=ordering)
    db.add(stage)
    db.flush()
    counters["stages"] += 1
    return stage


def find_team(db: Session, external_id: int | None, slug: str | None, name: str | None) -> Team | None:
    if external_id is not None:
        team = db.scalar(select(Team).where(Team.external_id == external_id))
        if team:
            return team

    if slug:
        team = db.scalar(select(Team).where(Team.slug == slug))
        if team:
            return team

    if name:
        return db.scalar(select(Team).where(Team.name == name))

    return None


def get_or_create_team(db: Session, team_data: dict | None, counters: dict[str, int]) -> Team | None:
    if not team_data:
        return None

    external_id = team_data.get("id")
    slug = team_data.get("slug")
    name = team_data.get("name")
    short_name = team_data.get("shortName")

    if external_id is None and not slug and not name:
        return None

    team = find_team(db, external_id=external_id, slug=slug, name=name)
    if team:
        if not team.short_name and short_name:
            team.short_name = short_name
        if not team.slug and slug:
            team.slug = slug
        if not team.external_id and external_id is not None:
            team.external_id = external_id
        return team

    team = Team(
        external_id=external_id,
        name=name or "Unknown Team",
        short_name=short_name,
        slug=slug,
    )
    db.add(team)
    db.flush()
    counters["teams"] += 1
    return team


def get_or_create_venue(db: Session, venue_name: str | None, counters: dict[str, int]) -> Venue | None:
    if not venue_name:
        return None

    venue = db.scalar(select(Venue).where(Venue.name == venue_name))
    if venue:
        return venue

    venue = Venue(name=venue_name)
    db.add(venue)
    db.flush()
    counters["venues"] += 1
    return venue


def create_result(db: Session, result_data: dict | None, counters: dict[str, int]) -> EventResult | None:
    if not result_data:
        return None

    result = EventResult(
        home_score=result_data.get("home"),
        away_score=result_data.get("away"),
        winner=result_data.get("winner"),
    )
    db.add(result)
    db.flush()
    counters["results"] += 1
    return result


def import_events(db: Session, events_data: Iterable[dict]) -> dict[str, int]:
    counters = {
        "events": 0,
        "competitions": 0,
        "stages": 0,
        "teams": 0,
        "venues": 0,
        "results": 0,
    }

    sport = get_or_create_sport(db, name="Football")

    for item in events_data:
        competition = get_or_create_competition(db, item, counters)
        stage = get_or_create_stage(db, item.get("stage"), counters)
        home_team = get_or_create_team(db, item.get("homeTeam"), counters)
        away_team = get_or_create_team(db, item.get("awayTeam"), counters)
        venue = get_or_create_venue(db, item.get("stadium"), counters)
        result = create_result(db, item.get("result"), counters)

        event = Event(
            season=item.get("season"),
            status=item.get("status") or "unknown",
            event_date=safe_parse_date(item.get("dateVenue")),
            event_time_utc=item.get("timeVenueUTC"),
            description=item.get("description"),
            source_payload_json=json.dumps(item, ensure_ascii=False),
            _sport_id=sport.id,
            _competition_id=competition.id if competition else None,
            _stage_id=stage.id if stage else None,
            _venue_id=venue.id if venue else None,
            _home_team_id=home_team.id if home_team else None,
            _away_team_id=away_team.id if away_team else None,
            _result_id=result.id if result else None,
        )
        db.add(event)
        counters["events"] += 1

    db.commit()
    return counters


def main() -> None:
    json_path = ROOT_DIR / "sample_data" / "events.json"

    if not json_path.exists():
        raise FileNotFoundError(f"Sample data file not found: {json_path}")

    print(f"Initializing database and importing from: {json_path}")
    init_db()

    events_data = load_events_json(json_path)

    with SessionLocal() as db:
        summary = import_events(db, events_data)

    print("Import complete:")
    print(f"- events imported: {summary['events']}")
    print(f"- competitions created: {summary['competitions']}")
    print(f"- stages created: {summary['stages']}")
    print(f"- teams created: {summary['teams']}")
    print(f"- venues created: {summary['venues']}")
    print(f"- results created: {summary['results']}")


if __name__ == "__main__":
    main()
