ROOT=docker
DEV=$(ROOT)/dev
STAGE=$(ROOT)/stage
ALEMBIC=$(ROOT)/alembic

CMD=docker-compose
UP_BUILD=up --build

all: dev-up

dev-up:
	cd $(DEV); $(CMD) $(UP_BUILD)

stage-up:
	cd $(STAGE); $(CMD) $(UP_BUILD)

dev-down:
	cd $(DEV); $(CMD) down

stage-down:
	cd $(STAGE); $(CMD) down

down: dev-down stage-down

alembic-dev:
	cd $(ALEMBIC); make dev

alembic-test:
	cd $(ALEMBIC); make test

startup:
	cp config.env.example docker/dev/config.env

.PHONY: dev-up stage-up down dev-down stage-down
