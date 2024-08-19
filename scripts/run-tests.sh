# Spinning up tests and deleteing the volumes when down.

pytest_args=$*
docker compose -f docker-compose.yml run --rm app-test $pytest_args
docker compose -f docker-compose.yml --profile test down --volumes
