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
  - `make install` — install dependencies using `uv sync --all-groups`
  - `make outdated` — check for outdated dependencies
  - `make format` — autoformat code with Ruff (fix and format)
  - `make lint` — check code style and errors with Ruff
  - `make typecheck` — run mypy with strict settings
  - `make test` or `make test-verbose` — run tests in Docker (pytest)
  - `make coverage` — run tests with coverage reporting (HTML + terminal)
  - `make shell` — enter a shell in the Glue container for debugging
  - `make checks` — run format, typecheck, and local tests
  - `make build` — build package wheel using `uv build`
  - `make publish` — publish to PyPI using `uv publish`
  - `make bumpver-*` — bump version (patch/minor/major/rc) using bumpver
  - `make release` — publish and tag a new release
  - `make checkov` — run Checkov security checks
  - `make prettier` — run Prettier code formatter
- **Tests** are in `test/` and run in a containerized environment for consistency with AWS Glue.
- **Dependencies** are managed with `uv` and grouped in `pyproject.toml` using `[dependency-groups]` (not `[project.optional-dependencies]`):
  - `dev` group: bumpver, mypy, ruff
  - `local` group: aws-glue-libs (from git), pyspark
  - `test` group: pytest, pytest-cov, pytest-randomly
- **Docker requirements**: `docker/requirements.txt` is auto-generated from `uv.lock` via `uv pip compile`
- **Prettier** and **Checkov** are available for formatting and security checks.

## Project Conventions & Patterns

- All source code is in `src/glue_utils/`.
- **Python version compatibility:**
  - All modules in `glue_utils.pyspark.*` must be Python 3.10+ compatible (Glue PySpark jobs run on 3.10+).
  - `glue_utils.helpers` and `glue_utils.options` must remain Python 3.9 compatible (Glue PythonShell scripts run on 3.9).
  - CI tests run against Python 3.9, 3.10, and 3.11 matrices (Glue PythonShell 3.9, Glue 4.0 3.10, Glue 5.0 3.11).
- **Type safety** is enforced via dataclasses and TypedDicts; avoid untyped dicts for options.
- **Connection patterns:** Use TypedDicts from `connection_options.py` and `format_options.py` for type-safe option passing.
- **BaseOptions usage:** Subclass `BaseOptions` for job argument parsing; all arguments start as strings with automatic type conversion in `__post_init__`.
- **Testing patterns:**
  - Mock `getResolvedOptions` for unit tests of option parsing.
  - Use `conftest.py` fixtures for shared test resources (e.g., `glue_pyspark_context`).
  - Test data source operations by mocking `create_dynamic_frame_from_options` and verifying call arguments.
  - Local tests (test/test_*.py) run without Docker container for faster feedback.
  - PySpark tests (test/pyspark/**) run in AWS Glue 5.0 container for environment parity.
- **Docker-based testing:** Tests run in AWS Glue 5.0 container (`public.ecr.aws/glue/aws-glue-libs:5`) for environment parity.
- **Linting:** Ruff with strict settings (select = ["ALL"]); mypy strict mode except for test code.
- **Versioning:** Use `make bumpver-*` commands; version is synced across pyproject.toml, README.md, src/glue_utils/__init__.py, and sonar-project.properties via bumpver.

## Architecture & Key Patterns

- **Modular design:** Context helpers are organized by data source in `src/glue_utils/pyspark/context/` (s3.py, dynamodb.py, jdbc.py, kafka.py, kinesis.py, mongodb.py, opensearch.py, documentdb.py).
- **TypedDict system:** Connection and format options use inheritance hierarchies (e.g., `S3SourceConnectionOptions` extends `BookmarkConnectionOptions`).
- **Generic job wrapper:** `GluePySparkJob[T]` is generic over `BaseOptions` subclasses for type-safe option access via `job.options`.
- **Automatic type conversion:** `BaseOptions` converts string arguments to annotated types in `__post_init__` with support for custom converters.
- **Method naming convention:** Context methods follow pattern `create_dynamic_frame_from_{source}_{format}` and `write_dynamic_frame_to_{sink}_{format}`.
- **Overloaded constructors:** `GluePySparkJob` uses `@overload` decorators to support multiple initialization patterns with proper type hints.

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
