# Testing

This project includes tests for the backend (pytest). The following commands describe how to run tests locally.

Backend
-------
Install dependencies and run tests with Poetry:

```bash
cd backend
poetry install
poetry run pytest -q
```

To run only unit or integration tests, use path selectors:

```bash
poetry run pytest tests/unit -q
poetry run pytest tests/integration -q
```

Collect coverage (example):

```bash
poetry run pytest --cov=app --cov-report=term-missing -q
```
