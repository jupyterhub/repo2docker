VERSION=$(shell git rev-parse --short HEAD)
IMAGE_PREFIX=jupyter/

build-image:
	docker build -t $(IMAGE_PREFIX)repo2docker:v$(VERSION) .

push-image:
	docker push $(IMAGE_PREFIX)repo2docker:v$(VERSION)

.all:
	build-image push-image
