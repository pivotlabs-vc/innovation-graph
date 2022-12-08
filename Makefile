
VERSION=$(shell git describe | sed 's/^v//')

all: data

data: challenges.db

challenges.db: challenges.ttl
	rdfproc -n -s sqlite challenges.db parse challenges.ttl turtle

REPO=europe-west1-docker.pkg.dev/pivot-labs/pivot-labs
WEB_CONTAINER=${REPO}/web:${VERSION}
SPARQL_CONTAINER=${REPO}/sparql:${VERSION}

images: data
	docker build -f Containerfile.web -t web .
	docker build -f Containerfile.sparql -t sparql .
	docker tag web ${WEB_CONTAINER}
	docker tag sparql ${SPARQL_CONTAINER}

push:
	docker push ${WEB_CONTAINER}
	docker push ${SPARQL_CONTAINER}

clean:
	-rm -f ${PROJECT}.db

	podman run -d --name web \
		-p 8080/tcp --expose=8080 \
		${WEB_CONTAINER}
	podman run -d --name sparql -p 8089/tcp \
		${SPARQL_CONTAINER}

stop:
	podman rm -f web sparql

