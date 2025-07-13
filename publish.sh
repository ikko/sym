#!/usr/bin/env python

set -e
set -x

twine check dist/*
twine upload dist/*
