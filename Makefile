setup:
	pip install poetry -q
	poetry install

test:
	pytest tests
