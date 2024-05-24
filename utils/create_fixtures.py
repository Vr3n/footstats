import json


continents = {
    "Asia": 0,
    "Africa": 1,
    "Europe": 2,
    "North America": 3,
    "South America": 4,
    "Oceania": 5,
    "Antarctica": 6,
}

with open("fixtures/utils/country-by-continent.json", 'r') as file:
    data = file.read()
    countries_by_continent = json.loads(data)


# Creating Continents fixture.
continents_fixture = [
    {
        "model": 'stats.continent',
        'pk': v,
        'fields': {
            'name': k,
            'slug': k.lower(),
        }
    }
    for k, v in continents.items()
]


# Creating Countries Fixture.
countries_fixture = []

for i, data in enumerate(countries_by_continent):
    tmp_data = dict()
    country, continent = data.values()
    tmp_data['model'] = 'stats.country'
    tmp_data['pk'] = i + 1
    tmp_data['fields'] = {
        'name': country,
        'slug': '-'.join(country.lower().split(' ')),
        'continent': continents[continent]
    }
    countries_fixture.append(tmp_data)


with open('fixtures/continent.json', 'w') as file:
    json.dump(continents_fixture, file)

with open('fixtures/country.json', 'w') as file:
    json.dump(countries_fixture, file)
