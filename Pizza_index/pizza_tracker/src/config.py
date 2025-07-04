# pizza_tracker/src/config.py

import os

CHROME_BINARY_LOCATION = os.environ.get("CHROME_BINARY_LOCATION")
CHROMEDRIVER_BINARY_LOCATION = os.environ.get("CHROMEDRIVER_BINARY_LOCATION")
DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://user:password@postgresserver/db")
