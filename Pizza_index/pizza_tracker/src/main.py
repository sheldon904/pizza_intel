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

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Mount the static files directory
app.mount("/static", StaticFiles(directory="web/static"), name="static")

@app.on_event("startup")
def startup_event():
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
async def get_status():
    # Placeholder for anomaly detection logic
    return {"status": "nominal"}

@app.get("/api/data")
async def get_data(db: Session = Depends(get_db)):
    return db.query(models.ScrapeData).all()

cli_app = typer.Typer()

@cli_app.command()
def scrape(url: str):
    """Scrape a single Google Maps URL for popular times."""
    print(f"Scraping {url}...")
    scraped_data = scraper.get_popular_times(url)
    
    if not scraped_data:
        print("No data scraped.")
        return

    # A very basic way to get a name from the URL provided in instructions.txt
    try:
        place_name = urllib.parse.unquote(url.split('query=')[1].split('&')[0])
    except IndexError:
        place_name = "Unknown"

    db = SessionLocal()
    try:
        for item in scraped_data:
            db_item = models.ScrapeData(
                place=place_name,
                url=url,
                scrape_time=datetime.now(),
                day_of_week=item['day_of_week'],
                hour_of_day=item['hour_of_day'],
                popularity_percent_normal=item['popularity_percent_normal'],
                popularity_percent_current=item.get('popularity_percent_current')
            )
            db.add(db_item)
        db.commit()
        print(f"Successfully saved {len(scraped_data)} records for '{place_name}' to the database.")
    except Exception as e:
        print(f"Error saving to database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    cli_app()
