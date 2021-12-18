setup:
	pip install -r requirements.txt
	pip install -e .

test:
	pytest tests -s --capture=no

dataset: nemde trading-price

nemde:
	nem -r nemde --start 2014-01-01 --end 2020-12-31

trading-price:
	nem -r trading-price --start 2014-01-01 --end 2020-12-31
