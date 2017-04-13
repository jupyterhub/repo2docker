
IMAGE_NAME = jupyterhub/singleuser-builder
VERSION = $(shell cat version)

.PHONY: build
build:
	docker build -t $(IMAGE_NAME):$(VERSION) .

.PHONY: test
test:
	docker build -t $(IMAGE_NAME)-candidate:$(VERSION) .
	IMAGE_NAME=$(IMAGE_NAME)-candidate:$(VERSION) test/run
