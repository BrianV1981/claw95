.PHONY: setup lint format typecheck test check run-server

setup:
	python3 -m venv .venv
	. .venv/bin/activate && pip install -U pip && pip install -e .[dev]

lint:
	. .venv/bin/activate && ruff check .

format:
	. .venv/bin/activate && ruff check . --fix

typecheck:
	. .venv/bin/activate && mypy src tests

test:
	. .venv/bin/activate && pytest -q

check: lint typecheck test

run-server:
	. .venv/bin/activate && python src/server.py
