from fastapi import FastAPI

from app.db import init_db
from app.routes.events import router as events_router

app = FastAPI(title="sports-calendar")
app.include_router(events_router)


@app.on_event("startup")
def on_startup() -> None:
    init_db()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
