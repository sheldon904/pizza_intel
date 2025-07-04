# pizza_tracker/src/config.py

import os

# Chrome/Selenium configuration
CHROME_BINARY_LOCATION = os.environ.get("CHROME_BINARY_LOCATION")
CHROMEDRIVER_BINARY_LOCATION = os.environ.get("CHROMEDRIVER_BINARY_LOCATION")

# Database configuration
DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://user:password@db:5432/pizza_tracker")
