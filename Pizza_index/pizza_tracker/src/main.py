# pizza_tracker/src/main.py

import typer
from fastapi import FastAPI, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from datetime import datetime
import urllib.parse

from . import scraper, models, scheduler
from .database import SessionLocal, engine

app = FastAPI()

# Mount the static files directory
app.mount("/static", StaticFiles(directory="web/static"), name="static")

@app.on_event("startup")
def startup_event():
    # Create database tables on startup
    models.Base.metadata.create_all(bind=engine)
    scheduler.start_scheduler()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", response_class=HTMLResponse)
async def read_root():
    with open("web/templates/index.html") as f:
        return f.read()

@app.get("/api/status")
async def get_status(db: Session = Depends(get_db)):
    latest_data = db.query(models.ScrapeData).order_by(models.ScrapeData.scrape_time.desc()).first()
    if latest_data and latest_data.popularity_percent_current is not None and latest_data.popularity_percent_normal is not None:
        if latest_data.popularity_percent_current > latest_data.popularity_percent_normal * 1.5:
            return {"status": "abnormal", "message": "anomaly detected – danger likely"}
    return {"status": "nominal", "message": "nominal busyness"}

@app.get("/api/data")
async def get_data(db: Session = Depends(get_db)):
    return db.query(models.ScrapeData).all()

cli_app = typer.Typer()

@cli_app.command()
def scrape(url: str):
    """Scrape a single Google Maps URL for popular times."""
    from .scheduler import scrape_url
    scrape_url(url)

if __name__ == "__main__":
    cli_app()
