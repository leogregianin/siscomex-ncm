test:
	poetry run pytest -vv --cov=.

lint:
	poetry run ruff check ./ncm/

mypy:
	poetry run mypy .

all:
	make test
	make lint
	make mypy
