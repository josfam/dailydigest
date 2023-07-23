import sqlite3
import random
from pathlib import Path
from dotenv import load_dotenv
import os
import requests
import json
from datetime import datetime as dt
from typing import Optional

load_dotenv()


def get_random_quote(quotes_db='quotes.db'):
    """Gets a random quote from the prepared sqlite database"""
    default_quote = '"Well begun is half done."\n— Aristotle'
    if not Path.exists(Path(quotes_db)):
        return default_quote
    try:
        conn = sqlite3.connect('quotes.db')
        cur = conn.cursor()
    except (sqlite3.OperationalError, sqlite3.DatabaseError):
        # return a default quote
        return default_quote
    else:
        get_quotes = """SELECT "quote", "author" FROM "quotes";"""
        with conn:
            cur.execute(get_quotes)
            quotes = cur.fetchall()
            quote, author = random.choice(quotes)
        return f'"{quote}"\n— {author}'


def get_weather_forecast(coords: dict = {'lat': 0.045, 'long': 32.447}) -> Optional[dict]:
    """Gets a 24-hour weather forecast for the location with the provided coordinates,
    by making API requests to `openweathermap`.

    Args:
        coords: The coordinates dictionary, with 'lat' and 'long' keys, that represents
        the location whose weather forecast to retrieve.
    Returns:
        A dictionary of various weather forecast data for the given location.
    """
    # Load an API key from a .env file
    API_KEY = os.getenv('OPEN_WEATHER_API_KEY')

    lat, long = coords['lat'], coords['long']
    params = f"lat={lat}&lon={long}&appid={API_KEY}&units=metric"
    url = f'https://api.openweathermap.org/data/2.5/forecast?{params}'

    try:
        response = requests.get(url)
        data = json.loads(response.text)
        forecast = {'city': data['city']['name'], 'country': data['city']['country'], 'forecasts': []}
    except Exception as e:
        print(e)
    else:
        for period in data['list'][0:9]:  # only interested in the one-day-ahead forecasts
            three_hr_forecast = {
                'timestamp': period['dt'],
                'temp': period['main']['temp'],
                'description': period['weather'][0]['description'].title(),
                'icon': f"https://openweathermap.org/img/wn/{period['weather'][0]['icon']}.png",
            }
            forecast['forecasts'].append(three_hr_forecast)

        return forecast
    return None


def get_twitter_trends():
    pass


def get_wikipedia_article():
    pass


if __name__ == "__main__":
    pass  # test code
