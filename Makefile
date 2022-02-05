.PHONY: init test lint security run run_dev migrate check build build_docker push


DJANGO_SETTINGS = \
	DJANGO_SETTINGS_MODULE=gitgrade.settings \
	SECRET_KEY=local

init:
	poetry install

test:
	$(DJANGO_SETTINGS) poetry run pytest


lint:
	poetry run black ./gitgrade ./repo
	poetry run mypy --strict ./
	$(DJANGO_SETTINGS) poetry run pylint --load-plugins pylint_django ./gitgrade ./repo
	hadolint Dockerfile
	poetry run yamllint docker-compose.yml

security:
	poetry export --without-hashes -f requirements.txt > tmp_requirements.txt
	poetry run liccheck -r tmp_requirements.txt
	poetry run safety check --full-report -r tmp_requirements.txt
	rm tmp_requirements.txt

run:
# Runs app as close to production as possible locally
	docker-compose up --build

run_dev:
	$(DJANGO_SETTINGS) poetry run python -m django runserver

migrate:
	$(DJANGO_SETTINGS) poetry run python -m django makemigrations
	$(DJANGO_SETTINGS) poetry run python -m django migrate

check: lint test security

build: init check
	poetry version > gitgrade/version.txt
	docker build --tag gitgrade:0.1.0 .

build_docker:
	docker build --tag gitgrade:0.1.0 .

push: init check
	aws ecr get-login-password --region us-west-2 \
		| docker login --username AWS --password-stdin 746433511096.dkr.ecr.us-west-2.amazonaws.com
	docker build --tag 746433511096.dkr.ecr.us-west-2.amazonaws.com/gitgrade:0.1.0 .
	docker push 746433511096.dkr.ecr.us-west-2.amazonaws.com/gitgrade:0.1.0

