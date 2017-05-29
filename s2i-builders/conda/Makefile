
IMAGE_NAME = jupyterhub/singleuser-builder-conda
VERSION = $(shell cat version)

.PHONY: build
build:
	docker build -t $(IMAGE_NAME):$(VERSION) .

push:
	docker push "$(IMAGE_NAME):$(VERSION)"
