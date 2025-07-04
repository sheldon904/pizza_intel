# pizza_tracker/src/scheduler.py

from apscheduler.schedulers.background import BackgroundScheduler
from .main import scrape # Import the scrape function

# URLs from instructions.txt
URLS_TO_SCRAPE = [
    "https://www.google.com/maps/search/?api=1&query=Domino%27s+Pizza+3535+S+Ball+St+Arlington+VA+22202",
    "https://www.google.com/maps/search/?api=1&query=Papa+John%27s+Pizza+2607+Columbia+Pike+Arlington+VA+22204",
    "https://www.google.com/maps/search/?api=1&query=District+Pizza+Palace+2325+S+Eads+St+Arlington+VA+22202",
    "https://www.google.com/maps/search/?api=1&query=Extreme+Pizza+1419+S+Fern+St+Arlington+VA+22202",
    "https://www.google.com/maps/search/?api=1&query=We%2C+The+Pizza+2100+Crystal+Dr+Arlington+VA+22202",
    "https://www.google.com/maps/search/?api=1&query=Freddie%27s+Beach+Bar+555+23rd+St+S+Arlington+VA+22202",
]

def schedule_scraping_jobs(scheduler: BackgroundScheduler):
    """Adds scraping jobs to the scheduler for each URL."""
    for url in URLS_TO_SCRAPE:
        # Schedule each job to run at a specified interval, e.g., every hour.
        # For demonstration, this is set to a long interval.
        # In a real application, this might be every hour or so.
        scheduler.add_job(scrape, 'interval', hours=24, args=[url], id=f"scrape_{url}", replace_existing=True)
        print(f"Scheduled scraping job for {url}")

def start_scheduler():
    """Initializes and starts the scheduler."""
    scheduler = BackgroundScheduler()
    schedule_scraping_jobs(scheduler)
    scheduler.start()
    print("Scheduler started.")
