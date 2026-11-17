.PHONY: install run test lint

install:
	python -m pip install -r requirements.txt

run:
	python -m depgraph --help

test:
	python -m pytest tests -v

lint:
	python -m flake8 src tests --max-line-length=80