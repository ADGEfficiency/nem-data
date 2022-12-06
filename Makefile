.PHONY: all clean setup test test-ci

all: test

setup:
	pip install poetry==1.2.2 -q
	poetry install -q

setup-test:
	poetry install --with test

test: setup-test
	pytest tests -s -x

test-ci: setup-test
	coverage run -m pytest tests --tb=short --show-capture=no
	coverage report -m

-include .env.secret
pypi:
	poetry build
	@poetry config pypi-token.pypi $(PYPITOKEN)
	poetry publish
