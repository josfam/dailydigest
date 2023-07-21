import sqlite3
import random
from pathlib import Path


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


def get_weather_forecast():
    pass


def get_twitter_trends():
    pass


def get_wikipedia_article():
    pass


if __name__ == "__main__":
    pass  # test code
