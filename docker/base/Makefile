TAG=teser/flask.base:latest

all: build_and_push

build_and_push:
	docker build -t $(TAG) -f flask/Dockerfile .
	docker push $(TAG)

pull:
	docker pull $(TAG)
