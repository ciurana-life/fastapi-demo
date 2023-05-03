FROM --platform=linux/amd64 python:3.10-slim

ENV PYTHONUNBUFFERED=1 \
    HOME_DIRECTORY=/code

# TODO needed ?
ENV VIRTUAL_ENV=${HOME_DIRECTORY}/.venv/ \
    PATH=${VIRTUAL_ENV}/bin:$PATH \
    PYTHONPATH=./src:$PYTHONPATH

# # RUN useradd -ms /bin/bash app
WORKDIR ${HOME_DIRECTORY}

RUN apt update && \
    apt install -y --no-install-recommends curl && \
    curl -sSL https://install.python-poetry.org | python -

ENV PATH=/root/.local/bin:$PATH
COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false
RUN poetry install

COPY ./app ${HOME_DIRECTORY}/app

# TODO There is an example on the docs with poetry

CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]