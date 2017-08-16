all: dev

dev:
    cd dev; docker-compose up --build

test:
    cd test; docker-compose up --build
