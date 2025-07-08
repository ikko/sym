SHELL := /bin/bash

.PHONY: install test lint build clean

VENV_PATH := $(HOME)/.virtualenvs/symbol

install:
	uv venv $(VENV_PATH)
	source $(HOME)/.virtualenvs/symbol/bin/activate
	python -m ensurepip
	python -m pip install -e .[dev]

test:
	PYTHONPATH=. $(VENV_PATH)/bin/python -m pytest tests

lint:
	ruff check .

build:
	uv build

clean:
	rm -rf dist build *.egg-info
