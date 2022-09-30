SRC = $(wildcard **/src/*.py)

.PHONY: deps dev-deps install

deps:
	pip install -r requirements.txt

dev-deps: deps
	pip install -r requirements-dev.txt

lock-requirements:
	pip freeze > requirements.lock

check-app:
	/bin/bash ci-static-app.sh

check: check-app

qa: check
