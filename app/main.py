import app.models  # noqa: F401 — ensures all models are registered with Base before create_all

from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.db.session import Base, engine
from app.routers import admin, applications, auth, companies, frontend, jobs

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Job Platform API")

app.mount(
    "/static",
    StaticFiles(directory=Path(__file__).parent / "front" / "static"),
    name="static",
)

# Frontend (HTML pages) — registered first so "/" serves the landing page
app.include_router(frontend.router)

# API routers
app.include_router(auth.router)
app.include_router(companies.router)
app.include_router(jobs.router)
app.include_router(applications.router)
app.include_router(admin.router)
