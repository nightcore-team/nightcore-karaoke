DOCKER_CONTAINER_NAME=bot
DOCKER_PROJECT_NAME=discord-bot-template
DOCKER_IMAGE_TAG=latest

d = docker
dc = docker compose
ur = uv run

.DEFAULT_GOAL := help

##@ Setup project
init: ## Initialize the project
	uv sync
	$(ur) pre-commit install --install-hooks
	$(ur) pre-commit autoupdate

##@ Local development
run: ## Run the application without Docker
	$(ur) __main__.py

lint: ## Run the linter
	$(ur) ruff check --config=pyproject.toml --fix ./src/

format: ## Format the code
	$(ur) ruff format --config=pyproject.toml ./src/

typecheck: ## Run the type checker
	$(ur) mypy --config-file=pyproject.toml ./src/

dev-logs: ## View development container logs
	$(d) logs -f $(DOCKER_CONTAINER_NAME)

dev-exec: ## Execute a command in the development container
	$(d) exec -it $(DOCKER_CONTAINER_NAME) /bin/bash

dev-bash: ## Start a bash session in the development container
	$(d) run --rm -it --env-file .env $(DOCKER_PROJECT_NAME):$(DOCKER_IMAGE_TAG) /bin/bash

dev-build: ## Build the development container
	$(dc) --env-file=.env build

dev-up: ## Start the development container
	$(dc) --env-file=.env up -d

dev-stop: ## Stop the development container
	$(dc) stop

dev-down: ## Stop and remove the development container
	$(dc) down

clean: ## Clean up the project (cache)
	find . -type d -name '__pycache__' -exec rm -rf {} +
	rm -rf .mypy_cache .ruff_cache .pytest_cache

##@ Git
commit: ## Do commit with conventional commit message
	$(ur) cz commit

bump: ## Bump the version and update CHANGELOG.md
	$(ur) cz bump

##@ Help
help: ## Show this help message
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

.PHONY: init commit bump help run lint format typecheck dev-logs dev-exec dev-bash dev-build dev-up dev-stop dev-down clean
