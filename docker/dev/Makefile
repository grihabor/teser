CMD=docker-compose

all: up

pull:
	$(CMD) pull

up: pull
	$(CMD) up --build

down:
	$(CMD) down

.PHONY: prod run pull
