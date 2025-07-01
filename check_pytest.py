import sys
import os

try:
    import pytest
    print(f"pytest found at: {pytest.__file__}")
except ImportError:
    print("pytest not found")

print(f"sys.path: {sys.path}")
print(f"os.environ['PATH']: {os.environ.get('PATH')}")
print(f"os.environ['VIRTUAL_ENV']: {os.environ.get('VIRTUAL_ENV')}")
