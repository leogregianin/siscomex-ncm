test:
	poetry run pytest -vv --cov=.

lint:
	poetry run flake8 ./ncm/

mypy:
	poetry run mypy .

all:
	make test
	make lint
	make mypy
