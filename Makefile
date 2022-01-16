PHONY: init test lint security run migrate check

init:
	poetry install

test:
	poetry run pytest


lint:
	poetry run black
	poetry run mypy --strict .
	poetry run pylint ./gitgrade ./repo

security:
	poetry export --without-hashes -f requirements.txt | poetry run safety check --full-report --stdin

run:
	poetry run django runserver

migrate:
	poetry run makemigrations
	poetry run migrate

check: lint test security

