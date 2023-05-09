# FastAPI base

## Required
[Docker](https://docs.docker.com/engine/install/)
[Poetry](https://python-poetry.org/docs/)
Make (if macos `brew install make`)

## Run with docker-compose
```
docker-compose up
```
Go to localhost:8000/docs


## Run without docker-compose
Install packages:
```
poetry update
```

From now one you can either run commands with `poetry COMMAND` or do `poetry shell`.

First comment the `DATABASE_URL` in `.env` and then run:
```
poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
This will make the app run with sqlite and generate a sql_app.db file.


## Other commands
Testing + coverage `pytest --cov=app --cov-report term-missing`
Make migrations:
```
docker-compose run app poetry run alembic revision --autogenerate -m "DESCRIPTION"
	docker-compose run app poetry run alembic upgrade head
```
