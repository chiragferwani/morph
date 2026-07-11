# Developer Guide

## Setting Up the Development Environment

```bash
# Clone the repo
git clone https://github.com/chiragferwani/morph.git
cd morph

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate   # Windows

# Install in development mode
pip install -e ".[all]"

# Install test dependencies
pip install pytest
```

## Code Style Guidelines

1. **Every function must have a docstring** explaining parameters and return values
2. **Add inline comments** for every important step
3. **Keep functions small** — one function does one thing
4. **Use meaningful variable names** — `page_title` not `pt`
5. **Avoid complex one-liners** — use simple loops
6. **Avoid OOP unless necessary** — prefer simple functions
7. **Handle all errors** with try/except and user-friendly messages

## Running Tests

```bash
# Run all tests
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/test_scrapers.py -v

# Run a single test
python -m pytest tests/test_utils.py::TestValidator::test_valid_https_url -v
```

## Adding a New Scraper

1. Create a new file in `morph/scrapers/` (e.g., `table_scraper.py`)
2. Follow the same pattern as existing scrapers
3. Add the function to `morph/__init__.py`
4. Add tests in `tests/test_scrapers.py`
5. Update the CLI in `morph/cli/main.py` if needed

## Adding a New Converter

1. Create a new file in `morph/converters/`
2. Handle missing dependencies gracefully with try/except imports
3. Add the function to `morph/__init__.py`
4. Add tests in `tests/test_converters.py`
