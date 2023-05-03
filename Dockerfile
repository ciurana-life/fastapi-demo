FROM --platform=linux/amd64 python:3.10

ENV PYTHONUNBUFFERED=1 \
    HOME_DIRECTORY=/code

ENV VIRTUAL_ENV=${HOME_DIRECTORY}/.venv/ \
    PATH=${VIRTUAL_ENV}/bin:$PATH \
    PYTHONPATH=${HOME_DIRECTORY}

WORKDIR ${HOME_DIRECTORY}

RUN curl -sSL https://install.python-poetry.org | python -

ENV PATH=/root/.local/bin:$PATH
COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false
# Current issue with 1.4.0 https://github.com/python-poetry/poetry/issues/7611
RUN poetry self update 1.3.0
RUN poetry install

COPY ./app ${HOME_DIRECTORY}/app
COPY .env ${HOME_DIRECTORY}
COPY ./migrations ${HOME_DIRECTORY}/migrations
COPY alembic.ini ${HOME_DIRECTORY}

EXPOSE 8000