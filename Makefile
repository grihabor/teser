ROOT=docker
DEV=$(ROOT)/dev
TEST=$(ROOT)/test
ALEMBIC=$(ROOT)/alembic

CMD=docker-compose
UP_BUILD=up --build

all: dev-up

dev-up:
	cd $(DEV); $(CMD) $(UP_BUILD)

test-up:
	cd $(TEST); $(CMD) $(UP_BUILD)

dev-down:
	cd $(DEV); $(CMD) down

test-down:
	cd $(TEST); $(CMD) down

down: dev-down test-down

alembic-dev:
	cd $(ALEMBIC); make dev

alembic-test:
	cd $(ALEMBIC); make test

startup:
	cp config.env.example docker/dev/config.env

.PHONY: dev-up test-up down dev-down test-down
