FROM python:3.9

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y --no-install-recommends curl \
    && curl -sSL https://install.python-poetry.org | python3.9 -
    
RUN pip install poetry

WORKDIR /app

RUN poetry new .

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

COPY requirements-docker.txt .

RUN poetry add $(cat requirements-docker.txt | xargs)

COPY . .

