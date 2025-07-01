SHELL := /bin/bash

.PHONY: install test lint build clean

VENV_PATH := /home/miki/.virtualenvs/symbol

install:
	uv pip install -e .[dev]

test:
	PYTHONPATH=. $(VENV_PATH)/bin/python -m pytest

lint:
	ruff check .

build:
	uv build

clean:
	rm -rf dist build *.egg-info
