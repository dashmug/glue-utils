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
	@docker compose run --build glue-utils-dev -c pytest


.PHONY: coverage
coverage: ## Generate test coverage HTML report
	@docker compose run --build glue-utils-dev -c "pytest --cov=src --cov-branch --cov-report=term --cov-report=html"


.PHONY: checks
checks: format typecheck test 


.PHONY: audit
audit: ## Audit dependencies for security issues
	@poetry check --lock
	@poetry run pip-audit --requirement requirements.txt


.PHONY: clean
clean: ## Delete generated artifacts
	@rm -rf __pycache__ .coverage .mypy_cache .pytest_cache .ruff_cache dist htmlcov
