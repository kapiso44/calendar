from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.crud import get_event_by_id, get_events
from app.db import get_db

router = APIRouter(tags=["pages"])
templates = Jinja2Templates(directory="app/templates")


@router.get("/")
def home(request: Request, db: Session = Depends(get_db)):
    events = get_events(db)
    return templates.TemplateResponse(
        request=request,
        name="events.html",
        context={"events": events, "page_title": "Events"},
    )


@router.get("/pages/events")
def events_page(request: Request, db: Session = Depends(get_db)):
    events = get_events(db)
    return templates.TemplateResponse(
        request=request,
        name="events.html",
        context={"events": events, "page_title": "Events"},
    )


@router.get("/pages/events/{event_id}")
def event_detail_page(event_id: int, request: Request, db: Session = Depends(get_db)):
    event = get_event_by_id(db, event_id)
    if not event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")

    return templates.TemplateResponse(
        request=request,
        name="event_detail.html",
        context={"event": event, "page_title": f"Event #{event.id}"},
    )
