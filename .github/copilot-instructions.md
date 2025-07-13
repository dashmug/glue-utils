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
- **Type safety** is enforced via dataclasses and TypedDicts; avoid untyped dicts for options.
- **Connection patterns:** Use TypedDicts from `connection_options.py` and `format_options.py` for type-safe option passing.
- **BaseOptions usage:** Subclass `BaseOptions` for job argument parsing; all arguments start as strings with automatic type conversion in `__post_init__`.
- **Testing patterns:**
  - Mock `getResolvedOptions` for unit tests of option parsing.
  - Use `conftest.py` fixtures for shared test resources (e.g., `glue_pyspark_context`).
  - Test data source operations by mocking `create_dynamic_frame_from_options` and verifying call arguments.
- **Docker-based testing:** Tests run in AWS Glue 5.0 container (`public.ecr.aws/glue/aws-glue-libs:5`) for environment parity.
- **Linting:** Ruff with strict settings; mypy strict mode except for test code.
- **Versioning:** Use `make bumpver-*` commands; version is managed across multiple files via `bumpver`.

## Architecture & Key Patterns

- **Modular design:** Context helpers are organized by data source in `src/glue_utils/pyspark/context/` (s3.py, dynamodb.py, etc).
- **TypedDict system:** Connection and format options use inheritance hierarchies (e.g., `S3SourceConnectionOptions` extends `BookmarkConnectionOptions`).
- **Generic job wrapper:** `GluePySparkJob[T]` is generic over `BaseOptions` subclasses for type-safe option access via `job.options`.
- **Automatic type conversion:** `BaseOptions` converts string arguments to annotated types in `__post_init__` with support for custom converters.
- **Method naming convention:** Context methods follow pattern `create_dynamic_frame_from_{source}_{format}` and `write_dynamic_frame_to_{sink}_{format}`.

## Integration Points

- **AWS Glue runtime:** Integrates with PySpark 3.5.4 and aws-glue-libs; expects these preinstalled in Glue environment.
- **Local development:** `local` dependency group provides aws-glue-libs from git and PySpark for IDE support.
- **Docker testing:** Uses official AWS Glue container for test environment parity.
- **CI/CD:** GitHub Actions for continuous integration (see `.github/workflows/`).
- **Package distribution:** Published to PyPI with version sync across pyproject.toml, README.md, and source files.

## Examples

- See `README.md` for usage patterns and code examples.
- See `test/` for test structure and coverage.
- Key test files: `test/test_options.py` for BaseOptions patterns, `test/pyspark/context/test_*.py` for data source examples.

---

For any new features, follow the patterns in `src/glue_utils/` and update tests in `test/` accordingly. Use the Makefile for all routine tasks. If unsure, check the README or existing code for examples.
