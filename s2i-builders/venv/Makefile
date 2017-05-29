IMAGE_PREFIX = jupyterhub/singleuser-builder-venv-
VERSION = $(shell cat version)

.PHONY: build
build:
	docker build -t $(IMAGE_PREFIX)3.5:$(VERSION) . -f Dockerfile
	docker build -t $(IMAGE_PREFIX)2.7:$(VERSION) . -f Dockerfile.py2

push:
	docker push "$(IMAGE_PREFIX)3.5:$(VERSION)"
	docker push "$(IMAGE_PREFIX)2.7:$(VERSION)"
