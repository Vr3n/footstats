import typing
import requests
import random
import gzip
from bs4 import BeautifulSoup


def load_data():
    user_agent_list = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
    ]
    user_agent = None

    for _ in range(1, 4):
        user_agent = random.choice(user_agent_list)

    headers = {
        'User-Agent': user_agent
    }

    # Requesting the tournaments.
    req = requests.get(
        "https://www.sofascore.com/sitemaps/hi_sitemap_tournaments_football.xml.gz",
        headers=headers)

    sitemap = gzip.decompress(req.content)

    soup = BeautifulSoup(sitemap, 'lxml')

    tournament_list = soup.findAll('xhtml:link')

    tournaments: typing.List[typing.Dict[str, str]] = list()

    for tournament in tournament_list:
        tmp_data = {}

        # If the language is not english. skip the tournament.
        lang = tournament.attrs['hreflang']
        if lang != 'en':
            continue

        # Cleaning up the torunament name.
        t = tournament.attrs['href'].split('/')
        tmp_data['id'] = t[-1]
        tmp_data['tournament_name'] = ' '.join(t[-2].split('-')).capitalize()
        tmp_data['tournament_slug'] = t[-2]
        tmp_data['tournament_category'] = t[-3]
        tournaments.append(tmp_data)

    print(tournaments)


if __name__ == "__main__":
    load_data()
