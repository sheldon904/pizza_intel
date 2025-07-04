# pizza_tracker/src/scheduler.py

from apscheduler.schedulers.background import BackgroundScheduler
from . import scraper
from .database import SessionLocal
from datetime import datetime
import urllib.parse

# URLs from instructions.txt
URLS_TO_SCRAPE = [
    "https://www.google.com/maps/search/?api=1&query=Domino%27s+Pizza+3535+S+Ball+St+Arlington+VA+22202",
    "https://www.google.com/maps/search/?api=1&query=Papa+John%27s+Pizza+2607+Columbia+Pike+Arlington+VA+22204",
    "https://www.google.com/maps/search/?api=1&query=District+Pizza+Palace+2325+S+Eads+St+Arlington+VA+22202",
    "https://www.google.com/maps/search/?api=1&query=Extreme+Pizza+1419+S+Fern+St+Arlington+VA+22202",
    "https://www.google.com/maps/search/?api=1&query=We%2C+The+Pizza+2100+Crystal+Dr+Arlington+VA+22202",
    "https://www.google.com/maps/search/?api=1&query=Freddie%27s+Beach+Bar+555+23rd+St+S+Arlington+VA+22202",
]

def scrape_url(url: str):
    """Scrape a single Google Maps URL for popular times."""
    print(f"Scraping {url}...")
    scraped_data = scraper.get_popular_times(url)
    
    if not scraped_data:
        print("No data scraped.")
        return

    # Extract place name from URL
    try:
        place_name = urllib.parse.unquote(url.split('query=')[1].split('&')[0])
    except IndexError:
        place_name = "Unknown"

    # Import models here to avoid circular imports
    from . import models
    
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

def schedule_scraping_jobs(scheduler: BackgroundScheduler):
    """Adds scraping jobs to the scheduler for each URL."""
    for url in URLS_TO_SCRAPE:
        # Schedule each job to run at a specified interval, e.g., every hour.
        # For demonstration, this is set to a long interval.
        # In a real application, this might be every hour or so.
        scheduler.add_job(scrape_url, 'interval', hours=24, args=[url], id=f"scrape_{url}", replace_existing=True)
        print(f"Scheduled scraping job for {url}")

def start_scheduler():
    """Initializes and starts the scheduler."""
    scheduler = BackgroundScheduler()
    schedule_scraping_jobs(scheduler)
    scheduler.start()
    print("Scheduler started.")
