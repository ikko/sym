# [`«symb»`](https://github.com/ikko/symb) cookbook

**Recipes for Symbolic Mastery**

_Recipe 1: How to Create a Mixin?_

---

# 1.6 Publishing Your Mixin: From Third-Party to Standard Library


> ⚠ _This module is under development and incomplete. Features may differ from what's written here. Should you use it, test comprehensively._
 


Once you've developed, tested, and documented your `symb` mixin, the next step is to make it available to others. This section outlines the process of publishing your mixin, from sharing it as a third-party package to potentially integrating it into the `symb` standard library.

## 1. As a Third-Party Package

The most common way to share your mixin is by packaging it as an independent Python library and publishing it to the Python Package Index (PyPI). This allows other developers to easily install and use your mixin via `pip`.

### Steps to Publish to PyPI:

1.  **Project Structure:** Organize your mixin code within a standard Python package structure. For example:

    ```
    my_symb_mixins/
    ├── my_symb_mixins/
    │   ├── __init__.py
    │   └── descendant_counter.py  # Your mixin code
    └── pyproject.toml             # Or setup.py
    └── README.md
    └── LICENSE
    ```

2.  **`pyproject.toml` (Recommended):** Use `pyproject.toml` for modern Python packaging. Define your project metadata, dependencies (e.g., `symb`, `anyio`, `pytest` for testing), and package information.

    ```toml
    # pyproject.toml example
    [project]
    name = "my-symb-mixins"
    version = "0.1.0"
    description = "Useful mixins for the symb framework"
    authors = [{name = "Your Name", email = "your.email@example.com"}]
    dependencies = [
        "symb",
        "anyio",
    ]

    [build-system]
    requires = ["setuptools>=61.0"]
    build-backend = "setuptools.build_meta"

    [project.optional-dependencies]
    dev = [
        "pytest",
        "pytest-anyio",
    ]
    ```

3.  **Build the Distribution:** Use `build` to create source and wheel distributions:

    ```bash
    pip install build
    python -m build
    ```

    This will create `dist/` directory containing `.tar.gz` and `.whl` files.

4.  **Upload to PyPI:** Use `twine` to upload your package. You'll need a PyPI account and an API token.

    ```bash
    pip install twine
    twine upload dist/*
    ```

    Your mixin will then be installable via `pip install my-symb-mixins`.

## 2. Contributing to the `symb` Standard Library

If your mixin provides fundamental functionality, is widely applicable, and meets the high quality standards of the `symb` project, you might consider contributing it to the `symb` standard library (e.g., `symb.builtins`).

### Criteria for Standard Library Inclusion:

*   **Broad Utility:** The mixin addresses a common need and is useful across a wide range of `symb` applications.
*   **High Quality:** Adheres to `symb`'s coding standards, includes comprehensive tests, and is well-documented.
*   **Performance:** Is optimized for performance and does not introduce significant overhead.
*   **Maintainability:** Is easy to understand, extend, and maintain by the core `symb` development team.
*   **No External Dependencies:** Ideally, standard library mixins should have minimal or no external dependencies beyond those already used by `symb` itself.

### Process for Contribution:

1.  **Open an Issue:** Start by opening an issue on the `symb` project's GitHub repository to discuss your proposed mixin and its potential inclusion. This allows for early feedback and alignment with the project's roadmap.
2.  **Develop and Test:** Ensure your mixin is fully developed, thoroughly tested, and well-documented, following all `symb` project guidelines.
3.  **Submit a Pull Request:** Create a pull request (PR) with your changes. The PR will undergo code review by the `symb` maintainers.
4.  **Address Feedback:** Be prepared to address feedback and make revisions based on the review process.

Contributing to the standard library is a significant way to impact the `symb` ecosystem and provide direct value to its users. Whether you publish as a third-party package or contribute to the core, sharing your mixins fosters a vibrant and collaborative community around the `symb` framework.
