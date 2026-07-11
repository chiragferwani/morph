# Publishing Guide

## Building the Package

```bash
# Install build tools
pip install build twine

# Build the package
python -m build

# This creates two files in the dist/ directory:
#   dist/morph_scraper-0.1.0.tar.gz      (source distribution)
#   dist/morph_scraper-0.1.0-py3-none-any.whl  (wheel)
```

## Publishing to TestPyPI (for testing)

```bash
# Upload to TestPyPI first
python -m twine upload --repository testpypi dist/*

# Test installing from TestPyPI
pip install --index-url https://test.pypi.org/simple/ morphscrapper
```

## Publishing to PyPI (production)

```bash
# Upload to the real PyPI
python -m twine upload dist/*

# Users can then install with:
pip install morphscrapper
```

## Versioning

We follow [Semantic Versioning](https://semver.org/):

- **MAJOR** (1.0.0) — Breaking changes
- **MINOR** (0.2.0) — New features, backwards compatible
- **PATCH** (0.1.1) — Bug fixes

Update the version in:
1. `morph/__init__.py` — `__version__`
2. `setup.py` — `version`
3. `pyproject.toml` — `version`
4. `CHANGELOG.md` — Add a new entry
