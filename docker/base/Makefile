TAG=grihabor/testing-server:base-flask

all: build_and_push

build_and_push:
	docker build -t $(TAG) .
	docker push $(TAG)

