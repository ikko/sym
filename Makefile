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
	echo "was 'ruff check --exit-zero . ' but because big disk size (11.6Mb around??) footprint"

build:
	uv build

clean:
	rm -rf dist build *.egg-info
