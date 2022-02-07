.PHONY: init test lint security run run_dev migrate check version build build_docker push_task push_image


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

version:
	poetry version | awk '{print $$2}' > gitgrade/version.txt


build_docker:
	docker build --tag gitgrade:$$(cat gitgrade/version.txt) .

build: init check version build_docker

push_image: init check
	aws ecr get-login-password --region us-west-2 \
		| docker login --username AWS --password-stdin 746433511096.dkr.ecr.us-west-2.amazonaws.com
	docker build --tag 746433511096.dkr.ecr.us-west-2.amazonaws.com/gitgrade:$$(cat gitgrade/version.txt) .
	docker push 746433511096.dkr.ecr.us-west-2.amazonaws.com/gitgrade:$$(cat gitgrade/version.txt)

push_task:
	aws ecs register-task-definition --cli-input-json file://aws/gitgrade-carrot.json

