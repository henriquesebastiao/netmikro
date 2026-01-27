lint:
	yamlfmt -lint -exclude .venv .
	mbake format --check Makefile
	ruff check .; ruff check . --diff
	mypy -p netmikro
	radon cc ./netmikro -a -na
	bandit -r ./netmikro

format:
	yamlfmt .
	mbake format Makefile
	ruff format .; ruff check . --fix

up:
	vagrant up

suspend:
	vagrant suspend

doc:
	mkdocs serve

test:
	yamlfmt -lint -exclude .venv .
	mbake format --check Makefile
	ruff check .; ruff check . --diff
	mypy -p netmikro
	radon cc ./netmikro -a -na
	bandit -r ./netmikro
	pytest -s -x --cov=netmikro -vv
	coverage html

export-requirements-doc:
	poetry export -f requirements.txt --output docs/requirements.txt --without-hashes --only doc

.PHONY: lint format up suspend doc test export-requirements-doc