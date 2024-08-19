import asyncio

from scraping.scrape_euro_league import extract_and_store_tournament_details

asyncio.run(extract_and_store_tournament_details())
