TAG = "MAKE"

help:
	@echo "The following make targets are available:"
	@echo ""
	@echo "	 datahub.cli\t		Execute datahub-cli"
	@echo "	 datahub.shell\t\t 	Access airflow-coordinator"
	@echo "	 airflow.shell\t\t 	Access airflow-cli"
	@echo ""
	@echo "	 compose.datahub\t\tRun datahub-related containers"
	@echo "	 compose.datahub.daemon\t\tRun datahub-related containers with daemon"
	@echo "	 compose.airflow\t\tRun airflow-related containers"
	@echo "	 compose.airflow.daemon\t\tRun airflow-related containers with daemon"
	@echo "	 compose.airflow.down\t\tRun airflow-related containers down"
	@echo ""
	@echo "	 check\t			Execute pre-commit hooks"
	@echo "	 changelog\t	 	Update 'CHANGELOG.md'"
	@echo ""

.PHONY: datahub.cli
datahub.cli:
	datahub --server http://localhost:8889

.PHONY: datahub.shell
datahub.shell:
	# docker exec -w /etc/trino -it trino /bin/bash

.PHONY: airflow.shell
airflow.shell:
	docker exec -it airflow-scheduler /bin/bash

.PHONY: mysql.shell
mysql.shell:
	mycli -u root -p admin                                                                                                                                                                                                                  │

.PHONY: compose.datahub
compose.datahub:
	COMPOSE_PROFILES=datahub docker-compose up

.PHONY: compose.datahub.daemon
compose.datahub.daemon:
	COMPOSE_PROFILES=datahub docker-compose up -d

.PHONY: compose.airflow
compose.airflow:
	COMPOSE_PROFILES=airflow docker-compose up

.PHONY: compose.airflow.daemon
compose.airflow.daemon:
	COMPOSE_PROFILES=airflow docker-compose up -d

.PHONY: compose.airflow.down
compose.airflow.down:
	COMPOSE_PROFILES=airflow docker-compose down

.PHONY: compose.clean
compose.clean:
	@ echo ""
	@ echo ""
	@ echo "[$(TAG)] ($(shell date '+%H:%M:%S')) - Cleaning container volumes ('docker/volume')"
	@ rm -rf docker/volume
	@ docker container prune -f
	@ docker volume prune -f
	@ echo ""
	@ echo ""

.PHONY:prepare
prepare:
	@ echo ""
	@ echo ""
	@ echo "[$(TAG)] ($(shell date '+%H:%M:%S')) - Prepare local environment"
	@ brew install pyenv pyenv-virtualenv
	@ pip3 install poetry
	@ pip3 install --upgrade pip
	@ poetry install
	@ pre-commit install
	@ pre-commit run
	@ echo ""
	@ echo ""

.PHONY:test
test:
	@ echo ""
	@ echo ""
	@ echo "[$(TAG)] ($(shell date '+%H:%M:%S')) - Executing tests"
	@ AIRFLOW_HOME=$(shell pwd) poetry run pytest dags-test/
	@ echo ""
	@ echo ""

.PHONY:check
check:
	@ echo ""
	@ echo ""
	@ echo "[$(TAG)] ($(shell date '+%H:%M:%S')) - Executing pre-commit hooks"
	@ pre-commit run
	@ echo ""
	@ echo ""

.PHONY: changelog
changelog:
	@ echo ""
	@ echo ""
	@ echo "[$(TAG)] ($(shell date '+%H:%M:%S')) - Updating CHANGELOG.md"
	@ $(git-changelog -bio CHANGELOG.md -c angular)
	@ echo ""
	@ echo ""