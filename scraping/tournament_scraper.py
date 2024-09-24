import asyncio
from typing import Dict, List
import httpx
import json

data = None

with open('./top_european_leagues.json', 'r') as f:
    data = json.load(f)


async def fetch_tournament(client: httpx.AsyncClient, url: str) -> None:
    resp = await client.get(url)
    if resp.status_code == 200 or resp.status_code == 201:
        print("Done!")


async def main(tournament_list: List[Dict]) -> None:
    async with httpx.AsyncClient() as client:
        tasks = []
        for tournament in tournament_list:
            tasks.append(
                fetch_tournament(
                    client,
                    f"http://127.0.0.1:8000/api/v1/scrape/tournaments?tournament_id={tournament['sofascore_id']}"
                )
            )

        await asyncio.gather(*tasks)


asyncio.run(main(data))
