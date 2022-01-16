PHONY: init test lint security run migrate check

init:
	poetry install

test:
	poetry run pytest


lint:
	poetry run black ./gitgrade ./repo
	poetry run mypy --strict ./
	poetry run pylint ./gitgrade ./repo

security:
	poetry export --without-hashes -f requirements.txt | poetry run safety check --full-report --stdin

run:
	DJANGO_SETTINGS_MODULE=gitgrade.settings poetry run python -m django runserver

migrate:
	poetry run python -m django makemigrations
	poetry run python -m django migrate

check: lint test security

