.PHONY: all clean setup test test-ci

all: test

clean:
	rm -rf ~/nem-data/data

setup:
	pip install pip -Uq
	pip install poetry==1.2.2 -q
	poetry install -q
setup-test: setup
	poetry install --with test
setup-check: setup
	poetry install --with check -q
setup-static: setup
	poetry install --with static -q

test: setup-test
	pytest tests -s -x --color=auto
test-ci: setup-test
	coverage run -m pytest tests --tb=short --show-capture=no
	coverage report -m

-include .env.secret
publish: setup
	poetry build
	@poetry config pypi-token.pypi $(PYPITOKEN)
	poetry publish

.PHONY: static
static: setup-static
	mypy **/*.py --config-file ./mypy.ini --pretty

.PHONY: format
format: setup-check
	isort **/*.py --profile black
	black **/*.py
	poetry lock --no-update

.PHONY: lint
lint: setup-check
	flake8 --extend-ignore E501
	isort --check **/*.py --profile black
	black --check **/*.py
	poetry lock --check

.PHONY: check
check: lint static
