ROOT=docker
DEV=$(ROOT)/dev
TEST=$(ROOT)/test

CMD=docker-compose
UP_BUILD=up --build
DOWN=down

all: dev

dev:
	cd $(DEV); $(CMD) $(UP_BUILD)

test:
	cd $(TEST); $(CMD) $(UP_BUILD)

dev-down:
	cd $(DEV); $(CMD) $(DOWN)

test-down:
	cd $(TEST); $(CMD) $(DOWN)

down: dev-down test-down

.PHONY: dev test down dev-down test-down
