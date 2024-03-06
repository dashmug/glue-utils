.PHONY: help
help: ## Show help (default)
	@echo "=== Glue Utils ==="
	@echo
	@echo "Available commands:"
	@grep --extended-regexp '^[ /.a-zA-Z0-9_-]+:.*?## .*$$' Makefile | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'


.PHONY: install
install: clean ## Create virtualenv and install dependencies
	@poetry install


.PHONY: outdated
outdated: ## Check for outdated dependencies
	@poetry show --latest --outdated


requirements.test.txt: poetry.lock
	@poetry export --with=dev --output requirements.test.txt


.PHONY: format
format: ## Format project source code
	@poetry run ruff check . --fix --unsafe-fixes
	@poetry run ruff format .


.PHONY: lint
lint: ## Check source code for common errors
	@poetry run ruff format . --check
	@poetry run ruff check .


.PHONY: typecheck
typecheck: ## Check type annotations
	@poetry run mypy


.PHONY: test
test: ## Run automated tests
	@docker compose run --rm --remove-orphans --build glue-utils -c pytest


.PHONY: coverage
coverage: ## Generate test coverage HTML report
	@docker compose run --rm --remove-orphans --build glue-utils -c "pytest --cov=glue_utils --cov-branch --cov-report=term --cov-report=html"


.PHONY: checks
checks: format typecheck test 


.PHONY: audit
audit: requirements.test.txt ## Audit dependencies for security issues
	@poetry check --lock
	@poetry run pip-audit --requirement requirements.test.txt


.PHONY: clean
clean: ## Delete generated artifacts
	@rm -rf __pycache__ .coverage .mypy_cache .pytest_cache .ruff_cache dist htmlcov
