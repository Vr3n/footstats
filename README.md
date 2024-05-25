# FootStats

Home for analyzing football statistics of tournaments, teams, and players.


## Running the Environment

1. Installing Initial Packages.

```bash

pip install -r requirements.txt
npm i

```

2. Migrations.

```bash

python manage.py makemigrations && pyhon manage.py migrate

```

3. Running the services.


- Django

```bash
python manage.py runserver

```

- Celery

```bash

celery -A core worker -l INFO

```

- Tailwindcss

```bash

 npx tailwindcss -i ./static/css/input.css -o static/css/styles.css --watch

```
