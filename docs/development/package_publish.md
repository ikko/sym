# Package Publication Guide

This document provides detailed instructions on how to build and publish the `symb` package to PyPI (Python Package Index) using `uv` and `twine`.

## Prerequisites

Before you begin, ensure you have the following installed:

*   **`uv`**: A fast Python package installer and resolver. If you don't have it, install it via `curl -LsSf https://astral.sh/uv/install.sh | sh`.
*   **`twine`**: A utility for uploading Python packages to PyPI. Install it using `pip install twine`.
*   **PyPI Account**: You need an account on [PyPI](https://pypi.org/) or [TestPyPI](https://test.pypi.org/).
*   **API Token**: For secure publishing, it is highly recommended to use an API token instead of your username and password. You can create an API token from your PyPI or TestPyPI account settings.

## Publication Steps

Follow these steps to build and publish the `symb` package:

### 1. Clean Build Artifacts

Before building, it's good practice to clean up any old build artifacts. This ensures a fresh build.

```bash
rm -rf build/ dist/ symb.egg-info/
```

Alternatively, the `publish.py` script handles this automatically.

### 2. Build the Package

Use `uv` to build the source distribution (`.tar.gz`) and the wheel distribution (`.whl`).

```bash
uv build
```

This command will create a `dist/` directory containing the generated package files.

### 3. Publish the Package

Use the `publish.py` script to upload your package. This script simplifies the process and allows you to easily switch between TestPyPI and the official PyPI.

#### Publishing to TestPyPI (Recommended for Testing)

It is highly recommended to test your publication process on [TestPyPI](https://test.pypi.org/) first. This allows you to verify that your package builds and uploads correctly without affecting the official PyPI.

```bash
python publish.py --test --username __token__ --password <your_testpypi_api_token>
```

Replace `<your_testpypi_api_token>` with your actual API token from TestPyPI.

#### Publishing to Official PyPI

Once you have successfully published to TestPyPI and are confident, you can publish to the official PyPI.

```bash
python publish.py --username __token__ --password <your_pypi_api_token>
```

Replace `<your_pypi_api_token>` with your actual API token from PyPI.

**Important Security Note**: Avoid typing your API token directly on the command line in shared environments. Consider using environment variables or a `.pypirc` file for better security.

## Verifying Publication

After successful publication, you can verify your package on:

*   **TestPyPI**: `https://test.pypi.org/project/symb/<version>`
*   **PyPI**: `https://pypi.org/project/symb/<version>`

Replace `<version>` with the actual version number of your package (e.g., `0.0.1`).

## Troubleshooting

*   **`twine` not found**: Ensure `twine` is installed (`pip install twine`).
*   **Authentication errors**: Double-check your username and API token. Ensure the token has the correct permissions for the repository you are targeting.
*   **No distribution files found**: Make sure `uv build` completed successfully and created files in the `dist/` directory.
*   **Package already exists**: If you are trying to upload a version that already exists on PyPI, you will get an error. Increment the version number in `pyproject.toml`.
