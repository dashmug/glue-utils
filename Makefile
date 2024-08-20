DOCKER_COMPOSE_RUN = USER_ID=$$(id -u) docker compose --file docker/docker-compose.yml run --rm --build glue-utils


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
	@poetry install --sync


.PHONY: outdated
outdated: ## Check for outdated dependencies
	@poetry show --latest --outdated


docker/requirements.txt: poetry.lock
	@poetry export --with=test --output docker/requirements.txt


.PHONY: format
format: ## Format project source code
	@poetry run ruff check . --fix
	@poetry run ruff format .


.PHONY: lint
lint: ## Check source code for common errors
	@poetry run ruff format . --check
	@poetry run ruff check .


.PHONY: typecheck
typecheck: ## Check type annotations
	@MYPYPATH=src poetry run mypy .


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


.PHONY: publish
publish: ## Publish package to PyPI
	@poetry publish --build


.PHONY: bumpver-rc
bumpver-rc: ## Bump release candidate
	@poetry run bumpver update --no-fetch --tag=rc --tag-num


.PHONY: bumpver-patch
bumpver-patch: ## Bump patch version
	@poetry run bumpver update --no-fetch --patch --tag=final


.PHONY: bumpver-minor
bumpver-minor: ## Bump minor version
	@poetry run bumpver update --no-fetch --minor --tag=final


.PHONY: bumpver-major
bumpver-major: ## Bump major version
	@poetry run bumpver update --no-fetch --major --tag=final


.PHONY: githooks
githooks: ## Install/update project git hooks
	@poetry run pre-commit install --install-hooks
	@poetry run pre-commit autoupdate
	@poetry run pre-commit run --all-files


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
