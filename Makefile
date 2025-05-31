DOCKER_COMPOSE_RUN = USER_ID=$$(id -u) COMPOSE_BAKE=true docker compose --file docker/docker-compose.yml run --rm --build glue-utils


.PHONY: help
help: ## Show help (default)
	@echo "=== Glue Utils ==="
	@echo
	@echo "Available commands:"
	@grep --extended-regexp '^[ /.a-zA-Z0-9_-]+:.*?## .*$$' Makefile | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'


.PHONY: all
 all: help


.PHONY: install
install: clean ## Create virtualenv and install dependencies
	@uv sync --all-groups


.PHONY: outdated
outdated: ## Check for outdated dependencies
	@uv pip list --outdated


docker/requirements.txt: uv.lock
	@uv pip compile --group test pyproject.toml --output-file docker/requirements.txt --generate-hashes


.PHONY: format
format: ## Format project source code
	@uv run ruff check . --fix
	@uv run ruff format .


.PHONY: lint
lint: ## Check source code for common errors
	@uv run ruff format . --check
	@uv run ruff check .


.PHONY: typecheck
typecheck: ## Check type annotations
	@MYPYPATH=src uv run mypy .


.PHONY: test
test: docker/requirements.txt ## Run automated tests
	@TARGET=test $(DOCKER_COMPOSE_RUN) -c pytest


.PHONY: test-verbose
test-verbose: docker/requirements.txt ## Run automated tests in verbose mode
	@TARGET=test $(DOCKER_COMPOSE_RUN) -c "pytest -vv"


.PHONY: coverage
coverage: docker/requirements.txt ## Run tests and measure code coverage
	@TARGET=coverage $(DOCKER_COMPOSE_RUN) -c "pytest --cov=glue_utils --cov-report=term --cov-report=html"


.PHONY: shell
shell: docker/requirements.txt ## Enter a shell in the container
	@$(DOCKER_COMPOSE_RUN) -c bash


.PHONY: checks
checks: format typecheck test


.PHONY: clean
clean: ## Delete generated artifacts
	@rm -rfv __pycache__ .coverage .import_linter_cache .mypy_cache .pytest_cache .ruff_cache coverage dist htmlcov test-results


.PHONY: build
build: clean  ## Build package wheel
	@uv build


.PHONY: publish
publish: ## Publish package to PyPI
	@uv publish


.PHONY: bumpver-rc
bumpver-rc: ## Bump release candidate
	@uv run bumpver update --no-fetch --tag=rc --tag-num


.PHONY: bumpver-patch
bumpver-patch: ## Bump patch version
	@uv run bumpver update --no-fetch --patch --tag=final


.PHONY: bumpver-minor
bumpver-minor: ## Bump minor version
	@uv run bumpver update --no-fetch --minor --tag=final


.PHONY: bumpver-major
bumpver-major: ## Bump major version
	@uv run bumpver update --no-fetch --major --tag=final


.PHONY: release
release: publish ## Publish and tag a new release
	@eval $$(bumpver show -n --environ) && git tag $$CURRENT_VERSION
	@git push --follow-tags
	@git push --tags


.PHONY: checkov
checkov: ## Run Checkov security checks
	@checkov -d .


.PHONY: prettier
prettier: clean  ## Run Prettier code formatter
	@prettier --write .
