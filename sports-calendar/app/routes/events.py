from fastapi import APIRouter

router = APIRouter(prefix="/events", tags=["events"])


@router.get("/")
def list_events_placeholder() -> dict[str, str]:
    return {"message": "Events endpoint placeholder"}
