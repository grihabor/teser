ROOT=docker
DEV=$(ROOT)/dev
TEST=$(ROOT)/test
ALEMBIC=$(ROOT)/alembic

CMD=docker-compose
UP_BUILD=up --build

all: dev

dev:
	cd $(DEV); $(CMD) $(UP_BUILD)

test:
	cd $(TEST); $(CMD) $(UP_BUILD)

dev-down:
	cd $(DEV); $(CMD) down

test-down:
	cd $(TEST); $(CMD) down

down: dev-down test-down

alembic:
	cd $(ALEMBIC); $(CMD) run bash

.PHONY: dev test down dev-down test-down
