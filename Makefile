SHELL := /bin/bash

.PHONY: install test lint build clean

VENV_PATH := $(HOME)/.virtualenvs/symb

install:
	uv venv $(VENV_PATH)
	source $(HOME)/.virtualenvs/symb/bin/activate
	python -m ensurepip
	python -m pip install -e .[dev]

test:
	PYTHONPATH=. $(VENV_PATH)/bin/python -m pytest

lint:
	ruff check --exit-zero .

build:
	uv build

clean:
	rm -rf dist build *.egg-info
