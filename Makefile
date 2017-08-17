all: dev

dev:
	cd dev; docker-compose up --build

test:
	cd test; docker-compose up --build

dev-down:
	cd dev; docker-compose down

test-down:
	cd test; docker-compose down

down: dev-down test-down

.PHONY: dev test down dev-down test-down
