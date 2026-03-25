from sqlalchemy import Date, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base


class Sport(Base):
    __tablename__ = "sports"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)

    events: Mapped[list["Event"]] = relationship(back_populates="sport")


class Competition(Base):
    __tablename__ = "competitions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    external_id: Mapped[int | None] = mapped_column(Integer, unique=True, nullable=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)

    events: Mapped[list["Event"]] = relationship(back_populates="competition")


class Stage(Base):
    __tablename__ = "stages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    external_id: Mapped[int | None] = mapped_column(Integer, unique=True, nullable=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    ordering: Mapped[int | None] = mapped_column(Integer, nullable=True)

    events: Mapped[list["Event"]] = relationship(back_populates="stage")


class Team(Base):
    __tablename__ = "teams"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    external_id: Mapped[int | None] = mapped_column(Integer, unique=True, nullable=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    short_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    slug: Mapped[str | None] = mapped_column(String(255), unique=True, nullable=True)

    home_events: Mapped[list["Event"]] = relationship(
        back_populates="home_team", foreign_keys="Event._home_team_id"
    )
    away_events: Mapped[list["Event"]] = relationship(
        back_populates="away_team", foreign_keys="Event._away_team_id"
    )


class Venue(Base):
    __tablename__ = "venues"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)

    events: Mapped[list["Event"]] = relationship(back_populates="venue")


class EventResult(Base):
    __tablename__ = "event_results"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    home_score: Mapped[int | None] = mapped_column(Integer, nullable=True)
    away_score: Mapped[int | None] = mapped_column(Integer, nullable=True)
    winner: Mapped[str | None] = mapped_column(String(50), nullable=True)

    events: Mapped[list["Event"]] = relationship(back_populates="result")


class Event(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    season: Mapped[str | None] = mapped_column(String(50), nullable=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False)
    event_date: Mapped[Date | None] = mapped_column(Date, nullable=True)
    event_time_utc: Mapped[str | None] = mapped_column(String(50), nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    source_payload_json: Mapped[str | None] = mapped_column(Text, nullable=True)

    _sport_id: Mapped[int] = mapped_column(ForeignKey("sports.id"), nullable=False)
    _competition_id: Mapped[int | None] = mapped_column(ForeignKey("competitions.id"), nullable=True)
    _stage_id: Mapped[int | None] = mapped_column(ForeignKey("stages.id"), nullable=True)
    _venue_id: Mapped[int | None] = mapped_column(ForeignKey("venues.id"), nullable=True)
    _home_team_id: Mapped[int | None] = mapped_column(ForeignKey("teams.id"), nullable=True)
    _away_team_id: Mapped[int | None] = mapped_column(ForeignKey("teams.id"), nullable=True)
    _result_id: Mapped[int | None] = mapped_column(ForeignKey("event_results.id"), nullable=True)

    sport: Mapped[Sport] = relationship(back_populates="events")
    competition: Mapped[Competition | None] = relationship(back_populates="events")
    stage: Mapped[Stage | None] = relationship(back_populates="events")
    venue: Mapped[Venue | None] = relationship(back_populates="events")
    home_team: Mapped[Team | None] = relationship(
        back_populates="home_events", foreign_keys=[_home_team_id]
    )
    away_team: Mapped[Team | None] = relationship(
        back_populates="away_events", foreign_keys=[_away_team_id]
    )
    result: Mapped[EventResult | None] = relationship(back_populates="events")
