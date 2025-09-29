
IMAGE=yoavklein3/http-recorder
CONTAINER_NAME=http-recorder
VERSION=0.1


.PHONY: build-image
build-image:
	docker build -t ${IMAGE}:${VERSION} .

.PHONY: push
push: build-image
	docker push ${IMAGE}:${VERSION}

.PHONY: run-container
run-container: build-image
	docker run --rm --name ${CONTAINER_NAME} -p 0.0.0.0:8090:5000 -d  ${IMAGE}:${VERSION}

.PHONY: stop-container
stop-container:
	docker container stop ${CONTAINER_NAME}
