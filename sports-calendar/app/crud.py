from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.models import Competition, Event, EventResult, Sport, Stage, Team, Venue
from app.schemas import EventCreate


def get_or_create_sport_by_name(db: Session, name: str = "Football") -> Sport:
    sport = db.scalar(select(Sport).where(Sport.name == name))
    if sport:
        return sport

    sport = Sport(name=name)
    db.add(sport)
    db.flush()
    return sport


def get_or_create_competition_by_name(db: Session, name: str | None) -> Competition | None:
    if not name:
        return None

    competition = db.scalar(select(Competition).where(Competition.name == name))
    if competition:
        return competition

    competition = Competition(name=name)
    db.add(competition)
    db.flush()
    return competition


def get_or_create_stage_by_name(db: Session, name: str | None, ordering: int | None = None) -> Stage | None:
    if not name:
        return None

    stage = db.scalar(select(Stage).where(Stage.name == name, Stage.ordering == ordering))
    if stage:
        return stage

    stage = Stage(name=name, ordering=ordering)
    db.add(stage)
    db.flush()
    return stage


def get_or_create_team_by_name(db: Session, name: str | None) -> Team | None:
    if not name:
        return None

    team = db.scalar(select(Team).where(Team.name == name))
    if team:
        return team

    team = Team(name=name)
    db.add(team)
    db.flush()
    return team


def get_or_create_venue_by_name(db: Session, name: str | None) -> Venue | None:
    if not name:
        return None

    venue = db.scalar(select(Venue).where(Venue.name == name))
    if venue:
        return venue

    venue = Venue(name=name)
    db.add(venue)
    db.flush()
    return venue


def maybe_create_result(db: Session, payload: EventCreate) -> EventResult | None:
    if payload.home_score is None and payload.away_score is None and not payload.winner:
        return None

    result = EventResult(
        home_score=payload.home_score,
        away_score=payload.away_score,
        winner=payload.winner,
    )
    db.add(result)
    db.flush()
    return result


def create_event(db: Session, payload: EventCreate) -> Event:
    sport = get_or_create_sport_by_name(db, payload.sport_name or "Football")
    competition = get_or_create_competition_by_name(db, payload.competition_name)
    stage = get_or_create_stage_by_name(db, payload.stage_name, payload.stage_ordering)
    venue = get_or_create_venue_by_name(db, payload.venue_name)
    home_team = get_or_create_team_by_name(db, payload.home_team_name)
    away_team = get_or_create_team_by_name(db, payload.away_team_name)
    result = maybe_create_result(db, payload)

    event = Event(
        season=payload.season,
        status=payload.status,
        event_date=payload.event_date,
        event_time_utc=payload.event_time_utc,
        description=payload.description,
        _sport_id=sport.id,
        _competition_id=competition.id if competition else None,
        _stage_id=stage.id if stage else None,
        _venue_id=venue.id if venue else None,
        _home_team_id=home_team.id if home_team else None,
        _away_team_id=away_team.id if away_team else None,
        _result_id=result.id if result else None,
    )
    db.add(event)
    db.commit()

    return get_event_by_id(db, event.id)  # return fully loaded relationships for response


def _event_with_relations_query():
    # Eager-load related tables in one ORM query plan to avoid N+1 lazy-load lookups.
    return (
        select(Event)
        .options(
            joinedload(Event.sport),
            joinedload(Event.competition),
            joinedload(Event.stage),
            joinedload(Event.venue),
            joinedload(Event.home_team),
            joinedload(Event.away_team),
            joinedload(Event.result),
        )
    )


def get_events(db: Session) -> list[Event]:
    query = _event_with_relations_query().order_by(Event.event_date, Event.id)
    return list(db.scalars(query).unique().all())


def get_event_by_id(db: Session, event_id: int) -> Event | None:
    query = _event_with_relations_query().where(Event.id == event_id)
    return db.scalars(query).unique().first()
