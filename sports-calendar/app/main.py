from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.db import init_db
from app.routes.events import router as events_router
from app.routes.pages import router as pages_router

app = FastAPI(title="sports-calendar")
app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.include_router(events_router)
app.include_router(pages_router)


@app.on_event("startup")
def on_startup() -> None:
    init_db()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
