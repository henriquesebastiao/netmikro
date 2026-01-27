lint:
	yamlfmt -lint -exclude .venv .
	mbake format --check Makefile
	ruff check .; ruff check . --diff

format:
	yamlfmt .
	mbake format Makefile
	ruff format .; ruff check . --fix

.PHONY: lint format