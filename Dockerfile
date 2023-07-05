# ---------------------------------------------------------------------
# build stage

FROM python:3.10-slim AS builder

ENV POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_NO_INTERACTION=1

# to run poetry directly as soon as it's installed
ENV PATH="$POETRY_HOME/bin:$PATH"

# install poetry
RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && curl -sSL https://install.python-poetry.org | python3 - \
    && chmod 755 ${POETRY_HOME}/bin/poetry

WORKDIR /app

# copy only pyproject.toml and poetry.lock file nothing else here
COPY poetry.lock pyproject.toml ./

# this will create the folder /app/.venv
RUN poetry install --only main --no-root --no-ansi --no-interaction

# ---------------------------------------------------------------------
# deployment stage

FROM python:3.10-slim

RUN apt-get update && apt-get install -y bash cron

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/app/.venv/bin:$PATH"

WORKDIR /app

# copy the venv folder from builder image 
COPY --from=builder /app/.venv ./.venv

COPY ./src/ ./src/
COPY ./conf/ ./conf/
COPY ./data/ ./data/
COPY ./crontab/ ./

# run wrapper script as entrypoint
RUN chmod +x /app/wrapper.sh
ENTRYPOINT ["/app/wrapper.sh"]