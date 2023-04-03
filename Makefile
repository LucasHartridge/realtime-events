ifneq (,$(wildcard ./.env))
	include .env
endif

setup-env: ## Setup the environment variables
ifeq (, $(shell which envsubst))
	$(error "No envsubst in $(PATH), consider doing apt-get install gettext-base (https://command-not-found.com/envsubst)")
endif	
	envsubst < .env.example > .env

docker-build: ## Docker build in detached mode
	@docker compose up --build -d

docker-delete: ## Docker delete images, volumes and its dependencies
	@docker compose down --rmi all --volumes

docker-prune: ## Docker image prune
	@docker image prune --force

docker-up: ## Docker compose up
	@docker compose up

docker-down: ## Docker compose down
	@docker compose down

start: docker-up ## Start application

stop: docker-down ## Stop application

install: docker-build ## Install application

uninstall: docker-delete docker-prune ## Uninstall application and its dependencies (images, volumes, networks)

recreate: uninstall install ## Recreate application
