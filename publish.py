import sys
import subprocess
import importlib
import importlib.metadata
import os
import csv
from pathlib import Path

# Get installed packages and their versions using importlib.metadata
installed_packages = {pkg.metadata['Name']: pkg.version for pkg in importlib.metadata.distributions()}


def get_package_size(package_name):
    """Use `du -h` to get the size of the package directory."""
    try:
        result = subprocess.run(
            ['du', '-sh', f"{sys.prefix}/lib/python{sys.version_info[0:3]}/site-packages/{package_name}"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        size = result.stdout.decode('utf-8').split()[0]
        return size
    except Exception as e:
        return "0.00 MB"


def get_package_info(package_name):
    """Get detailed info about an installed package."""

    # Get the package version
    version = installed_packages.get(package_name, "Unknown")

    # Get the import name (usually same as the package name)
    try:
        package = importlib.import_module(package_name)
        import_name = package.__name__
    except ImportError:
        import_name = "N/A"

    # Get package size using du -h
    size = get_package_size(package_name)

    # Show import name only if it does not match package name
    import_name_str = f"Import Name: {import_name}" if import_name != package_name else ""

    return f"{package_name},{import_name_str},{version},{size}"


def print_package_info():
    """Print information for each installed package."""
    print("Package Name,Import Name,Version,Size")
    for package_name in installed_packages:
        info = get_package_info(package_name)
        print(info)


if __name__ == "__main__":
    print_package_info()
