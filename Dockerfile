FROM python:3.10-bullseye

# Lots of ideas borrowed from:
# https://testdriven.io/blog/dockerizing-django-with-postgres-gunicorn-and-nginx/

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
      cloc=1.86-1 \
      postgresql-client=13+225 \
    && apt-get autoremove \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir --upgrade pip==22.0.2 \
    && pip install --no-cache-dir poetry==1.1.12

COPY gitgrade /code/gitgrade
COPY authorization /code/authorization
COPY repo /code/repo

COPY poetry.lock \
     pyproject.toml \
     manage.py \
     docker-wait.sh \
     /code/

WORKDIR /code

RUN poetry config virtualenvs.create false \
    && poetry install --no-dev \
    && adduser --no-create-home --disabled-password --shell /sbin/nologin gitgrade \
    && chown -R gitgrade /code

USER gitgrade
CMD ["/code/docker-wait.sh", "uwsgi", "--http", ":8000", "--module", "gitgrade.wsgi"]
