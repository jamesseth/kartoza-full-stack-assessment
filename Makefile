ifeq ($(UNAME),Darwin)
	SHELL := /opt/local/bin/bash
	OS_X  := true
else ifneq (,$(wildcard /etc/redhat-release))
	OS_RHEL := true
else
	OS_DEB  := true
	SHELL := /bin/bash
endif


ifneq (,$(wildcard ./.env))
include .env
export
else
include .env.template
export
endif

override PROJECT_ID=$$(basename `git rev-parse --show-toplevel`)

ifndef IS_LOCAL
override IS_LOCAL=True
endif

.EXPORT_ALL_VARIABLES:


## ==
.PHONY: help
help: ## Prints help for targets with comments.
	@cat $(MAKEFILE_LIST) \
		| grep -E '^[a-zA-Z_-]+:.*?## .*$$' \
		| awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

## ==

.PHONY: build
build: Dockerfile docker-compose.yml ## Build docker images.
	[ ! -f .env ] && cp .env.template .env || true;
	docker build -t "$(PROJECT_ID)-postgis" ./Dockerfile.postgis
	docker-compose -p "$(PROJECT_ID)" build

.PHONY: start
start: ## Start Containers.
	docker-compose -p $(PROJECT_ID) -f docker-compose.yml up --remove-orphans --build -d

.PHONY: stop
stop: ## Stop containers.
	docker-compose -p $(PROJECT_ID) -f docker-compose.yml down --remove-orphans

.PHONY: restart
restart: ## Restart containers.
	make stop && make start

.PHONY: logs
logs: ## Start Containers.
	docker-compose -p $(PROJECT_ID) -f docker-compose.yml logs -f

.PHONY: attach
attach: ## Attach to docker-compose services eg.. make attach DC=django
	docker exec -it \
	$($(SHELL) docker ps -f name="$(PROJECT_ID)_$(DC)" --format "{{.ID}}") bash

.PHONY: pre-commit
pre-commit: ## Run pre-commits.
	[[ $$(pip3 list | grep pre-commit) ]] && true || pip3 install pre-commit
	pre-commit run -a

.PHONY: create-app
create-app: ## Create a new Django app.
	docker-compose -p $(PROJECT_ID) -f docker-compose.yml run django sh -c "python3 manage.py startapp $(APP_NAME)"

.PHONY: migrations
migrations: ## Django make Migration
	docker-compose -p $(PROJECT_ID) -f docker-compose.yml run django sh -c "python3 manage.py makemigrations && python3 manage.py migrate"

.PHONY: test
test: ## Run Django unit-tests.
	docker-compose -p $(PROJECT_ID) -f docker-compose.yml run django sh -c "python3 manage.py test"

.PHONY: ingest
ingest:
	ogr2ogr -update -append -progress -f PostgreSQL PG:"dbname=$(DJANGO_DB_NAME) host=$(DJANGO_DB_HOST) user=$(DJANGO_DB_USER) password=$(DJANGO_DB_PASS) port=$(DJANGO_DB_PORT)" "$(FILE_PATH)"

.PHONY: export-to-gpkg
export-to-gpkg:

	set -x && docker-compose exec django sh -c 'ogr2ogr -f GPKG $(OUTPUT_FILE) "PG:host=$(DJANGO_DB_HOST) dbname=$(DJANGO_DB_DATABASE) user=$(DJANGO_DB_USERNAME) password=$(DJANGO_DB_PASSWORD) port=$(DJANGO_DB_PORT) " -sql "select * from spikey_polygons"'
