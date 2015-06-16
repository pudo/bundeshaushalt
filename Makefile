PY=env/bin/python
PIP=env/bin/pip

all: scrape dump

env/bin/python:
	virtualenv env
	$(PIP) install -r requirements.txt

scrape: env/bin/python
	$(PY) scraper.py

dump: env/bin/python
	env/bin/datafreeze dump.yaml

clean:
	rm -rf data/*.csv
	rm -f data.sqlite
