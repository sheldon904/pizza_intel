# pizza_tracker/src/scraper.py

import os
import urllib.parse
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service as ChromeService
from bs4 import BeautifulSoup
from datetime import datetime
from typing import List, Dict, Any, Optional

from . import config

# gmaps starts their weeks on sunday
days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

def get_popular_times(url: str) -> List[Dict[str, Any]]:
    """
    Scrapes the popular times data for a given Google Maps URL.
    """
    html = get_html(url)
    if html:
        return parse_html(html)
    return []

def get_html(u: str) -> Optional[str]:
    """
    Gets the HTML source of a Google Maps page.
    """
    try:
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--lang=de-DE') # Use German for 24h time format
        if config.CHROME_BINARY_LOCATION:
            options.binary_location = config.CHROME_BINARY_LOCATION
        
        # The path to chromedriver can be set in the system's PATH or specified here.
        # If CHROMEDRIVER_BINARY_LOCATION is not set, Selenium will try to find it in PATH.
        if config.CHROMEDRIVER_BINARY_LOCATION:
            d = webdriver.Chrome(service=ChromeService(config.CHROMEDRIVER_BINARY_LOCATION), options=options)
        else:
            # This relies on chromedriver being in the system's PATH
            d = webdriver.Chrome(options=options)


        d.get(u)

        # Wait for the popular times bars to be present
        WebDriverWait(d, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'section-popular-times-bar'))
        )

        html = d.page_source
        d.quit()
        return html

    except TimeoutException:
        print(f'ERROR: Timeout! (This could be due to missing "popular times" data, or not enough waiting.) for url: {u}')
        return None
    except Exception as e:
        print(f"An error occurred in get_html: {e}")
        if 'd' in locals():
            d.quit()
        return None


def parse_html(html: str) -> List[Dict[str, Any]]:
    """
    Parses the HTML to extract popular times data.
    """
    soup = BeautifulSoup(html, features='html.parser')
    pops = soup.find_all('div', {'class': 'section-popular-times-bar'})

    data = []
    dow = 0
    hour = 0

    for pop in pops:
        t = pop['aria-label']
        hour_prev = hour
        freq_now = None

        try:
            if 'normal' not in t:
                hour = int(t.split()[1])
                freq = int(t.split()[4])
            else:
                # The current hour has special text
                hour = hour + 1
                freq = int(t.split()[-2])
                try:
                    freq_now = int(t.split()[2])
                except (ValueError, IndexError):
                    freq_now = None # Not always present

            if hour < hour_prev:
                dow += 1

            data.append({
                "day_of_week": days[dow % 7],
                "hour_of_day": hour,
                "popularity_percent_normal": freq,
                "popularity_percent_current": freq_now
            })

        except (ValueError, IndexError) as e:
            # This can happen if the place is closed on that day
            print(f"Could not parse popular times for a day, skipping. Error: {e}")
            dow += 1
            continue
            
    return data
