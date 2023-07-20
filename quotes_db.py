"""Preparation script that"""

import requests
import time
import json
from pathlib import Path
import sqlite3
from pprint import pprint

LIMIT = 5
QUOTE_NUMBER = 500 // LIMIT
API_WAIT_TIME = 80  # seconds
REQUESTS_EXCEPTION_WAIT_TIME = 10  # seconds


# retrieve many quotes (could contain duplicates) from the `quotable` API
if not Path.exists(Path('quote_chunks.txt')):
    quote_data = []
    tags = 'Inspirational|Motivational|Success|Self Help'
    chunks_added = 0

    while True:
        if chunks_added == QUOTE_NUMBER:
            break
        try:
            r = requests.get(f'https://api.quotable.io/quotes/random?limit=5?tags={tags}')

            # wait for over a minute if the rate limit has been exceeded
            if r.status_code == 429:
                print('API rate limit exceeded')
                print(f'Waiting {API_WAIT_TIME} seconds, before trying again...')
                time.sleep(API_WAIT_TIME)
        except KeyboardInterrupt:
            print('Quote chunks interrupted ...')
            break
        except requests.RequestException:
            print('There was a requests exception')
            print(f'Waiting {REQUESTS_EXCEPTION_WAIT_TIME} seconds, before trying again...')
            time.sleep(REQUESTS_EXCEPTION_WAIT_TIME)
        else:
            quote_data.append(json.loads(r.text))
            chunks_added += 1
            print(f'Quote chunk {chunks_added}/{QUOTE_NUMBER} added...')

    # write the quote data to a file for later processing
    with open('quote_chunks.txt', 'w', encoding='utf8') as f:
        json.dump(quote_data, f)
        print('Quote chunks were written to file...')

if Path.exists(Path('quotes.db')):
    exit('Quotes database already exists')

# remove duplicate quotes
quote_ids = set()
unique_quotes = []

with open('quote_chunks.txt', 'r', encoding='utf8') as f:
    quotes = json.load(f)

for chunk in quotes:
    for quote in chunk:
        quote_id = quote['_id']
        if quote_id in quote_ids:
            continue
        unique_quotes.append(quote)
        quote_ids.add(quote_id)

# load unique quotes into a sqlite database
conn = sqlite3.connect('quotes.db')
cur = conn.cursor()

add_table = """CREATE TABLE IF NOT EXISTS "quotes" (
    "quote" TEXT NOT NULL,
    "author" TEXT NOT NULL
);"""

with conn:
    cur.execute(add_table)

with conn:
    for quote in unique_quotes:
        text = quote['content'].strip()
        author = quote['author'].strip()
        add_information = """INSERT INTO "quotes" ("quote", "author") VALUES(?, ?)
        """
        cur.execute(add_information, (text, author))
