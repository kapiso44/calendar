from datetime import date

from pydantic import BaseModel, ConfigDict, Field


class SportRead(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class CompetitionRead(BaseModel):
    id: int
    name: str
    external_id: int | None = None

    model_config = ConfigDict(from_attributes=True)


class StageRead(BaseModel):
    id: int
    name: str
    ordering: int | None = None
    external_id: int | None = None

    model_config = ConfigDict(from_attributes=True)


class TeamRead(BaseModel):
    id: int
    name: str
    short_name: str | None = None

    model_config = ConfigDict(from_attributes=True)


class VenueRead(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class EventResultRead(BaseModel):
    id: int
    home_score: int | None = None
    away_score: int | None = None
    winner: str | None = None

    model_config = ConfigDict(from_attributes=True)


class EventCreate(BaseModel):
    season: str | None = None
    status: str
    event_date: date | None = None
    event_time_utc: str | None = None
    description: str | None = None
    sport_name: str | None = Field(default="Football")
    competition_name: str | None = None
    stage_name: str | None = None
    stage_ordering: int | None = None
    venue_name: str | None = None
    home_team_name: str | None = None
    away_team_name: str | None = None
    home_score: int | None = None
    away_score: int | None = None
    winner: str | None = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
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
            }
        }
    )


class EventRead(BaseModel):
    id: int
    season: str | None = None
    status: str
    event_date: date | None = None
    event_time_utc: str | None = None
    description: str | None = None
    sport: SportRead
    competition: CompetitionRead | None = None
    stage: StageRead | None = None
    venue: VenueRead | None = None
    home_team: TeamRead | None = None
    away_team: TeamRead | None = None
    result: EventResultRead | None = None

    model_config = ConfigDict(from_attributes=True)
