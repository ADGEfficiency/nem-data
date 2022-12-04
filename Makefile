.PHONY: all clean setup test test-ci

all: test

setup:
	pip install -r requirements.txt -q
	pip install -e . -q

test: setup
	pytest tests -s --capture=no

test-ci: test
