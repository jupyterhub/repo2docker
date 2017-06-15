IMAGE_PREFIX = jupyterhub/singleuser-builder-julia
VERSION = $(shell cat version)

.PHONY: build
build:
	docker build -t $(IMAGE_PREFIX):$(VERSION) . -f Dockerfile

push:
	docker push "$(IMAGE_PREFIX):$(VERSION)"
