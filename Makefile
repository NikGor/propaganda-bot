install:
	poetry install

test:
	python manage.py test

lint:
	poetry run flake8

build:
	poetry build

selfcheck:
	poetry check

amend-and-push:
	git add .
	git commit --amend --no-edit
	git push --force

dev:
	export FLASK_APP=converter.api
	export FLASK_ENV=development
	flask run

migrate:
	python manage.py makemigrations
	python manage.py migrate

start:
	python manage.py runserver

ALL: lint install build



