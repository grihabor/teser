all: run

pull:
	docker-compose pull

run:
	docker-compose up

prod:
	docker-compose -f prod.yml up
