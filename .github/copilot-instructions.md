# Copilot Instructions for glue-utils

## Project Overview

- **glue-utils** is a Python library for AWS Glue ETL and Python Shell jobs, focused on reducing boilerplate, increasing type safety, and improving developer experience.
- Major components:
  - `BaseOptions`: Dataclass for parsing and type-casting command-line/job arguments.
  - `GluePySparkContext`: Subclass of `GlueContext` with type-safe helpers for common AWS data sources/sinks (S3, RDBMS, DynamoDB, Kinesis, Kafka, OpenSearch, DocumentDB, MongoDB, etc).
  - `GluePySparkJob`: Orchestrates job setup, context, and options, reducing boilerplate for typical Glue jobs.
  - TypedDicts for connection/format options in `src/glue_utils/pyspark/connection_options.py` and `format_options.py`.

## Developer Workflows

- **Build, test, and lint** are managed via the Makefile and Docker Compose:
  - `make install` — install dependencies in a virtualenv
  - `make format` — autoformat code with Ruff
  - `make lint` — check code style and errors
  - `make typecheck` — run mypy with strict settings
  - `make test` or `make test-verbose` — run tests in Docker (pytest)
  - `make coverage` — run tests with coverage reporting
  - `make build` — build package wheel
  - `make publish` — publish to PyPI
  - `make checks` — run format, typecheck, and tests
  - `make bumpver-*` — bump version (patch/minor/major/rc) using bumpver
- **Tests** are in `test/` and run in a containerized environment for consistency with AWS Glue.
- **Dependencies** are managed with `uv` and grouped in `pyproject.toml` (`dev`, `local`, `test`).
- **Prettier** and **Checkov** are available for formatting and security checks.

## Project Conventions & Patterns

- All source code is in `src/glue_utils/`.
- **Python version compatibility:**
  - All modules in `glue_utils.pyspark.*` must be Python 3.10+ compatible (Glue PySpark jobs run on 3.10+).
  - `glue_utils.helpers` and `glue_utils.options` must remain Python 3.9 compatible (Glue PythonShell scripts run on 3.9).
- Type safety is enforced via dataclasses and TypedDicts; avoid untyped dicts for options.
- Use the provided helpers for all Glue context/data source operations; do not reimplement connection logic.
- Prefer subclassing `BaseOptions` for job argument parsing.
- All arguments are parsed as strings; type conversion is handled in `BaseOptions`.
- Linting and formatting use Ruff; mypy is strict except for test code.
- Tests for each data source/context are in `test/pyspark/context/`.
- Use the Makefile for all build/test/lint/versioning tasks; do not run commands manually unless debugging.

## Integration Points

- Integrates with AWS Glue runtime (PySpark, Python Shell jobs).
- Expects `pyspark` and `aws-glue-libs` to be preinstalled in Glue, but provides a `local` dependency group for local dev.
- Docker Compose is used for local test/dev parity.
- CI/CD is configured via GitHub Actions (see `.github/workflows/`).

## Examples

- See `README.md` for usage patterns and code examples.
- See `test/` for test structure and coverage.

---

For any new features, follow the patterns in `src/glue_utils/` and update tests in `test/` accordingly. Use the Makefile for all routine tasks. If unsure, check the README or existing code for examples.
