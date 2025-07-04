# Pizza Tracker

A service for scraping and analyzing Google Maps popular times for pizza places.

## Usage

### Local Development

1.  Start the services:
    ```bash
    docker-compose up -d
    ```

2.  Run one-off scrapes:
    ```bash
    docker-compose exec web python src/main.py scrape <URL>
    ```

### API

-   `GET /api/status`: Returns the current status (nominal or anomaly).
-   `GET /api/data`: Returns the time-series data for all scraped locations.

