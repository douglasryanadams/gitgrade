PHONY: init test lint security run migrate check


DJANGO_SETTINGS = DJANGO_SETTINGS_MODULE=gitgrade.settings SECRET_KEY='local'

init:
	poetry install

test:
	$(DJANGO_SETTINGS) poetry run pytest


lint:
	poetry run black ./gitgrade ./repo
	poetry run mypy --strict ./
	$(DJANGO_SETTINGS) poetry run pylint --load-plugins pylint_django ./gitgrade ./repo

security:
	poetry export --without-hashes -f requirements.txt > tmp_requirements.txt
	poetry run liccheck -r tmp_requirements.txt
	poetry run safety check --full-report -r tmp_requirements.txt
	rm tmp_requirements.txt

run:
	$(DJANGO_SETTINGS) poetry run python -m django runserver

migrate:
	$(DJANGO_SETTINGS) poetry run python -m django makemigrations
	$(DJANGO_SETTINGS) poetry run python -m django migrate

check: lint test security

build:
	poetry version > gitgrade/version.txt
	# TODO
