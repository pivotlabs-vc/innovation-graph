
VERSION=$(shell git describe | sed 's/^v//')
SPARQL_EXPLORER_VERSION=0.4.2

PROJECT=challenges

all: sparql-explorer sparql
	rdfproc -n -s sqlite ${PROJECT}.db parse ${PROJECT}.ttl turtle

clean:
	-rm -rf sparql-explorer
	-rm -f sparql
	-rm -rf sparql-service
	-rm -f ${PROJECT}.db

serve:
	go build proxy/serve.go

sparql-explorer:
	-rm -rf sparql-explorer
	git clone git@github.com:cybermaggedon/sparql-explorer sparql-explorer
	(cd sparql-explorer; git checkout v${SPARQL_EXPLORER_VERSION})
	(cd sparql-explorer && npm install && ng build)

sparql:
	-rm -rf sparql-service
	git clone http://github.com/cybermaggedon/sparql-service
	(cd sparql-service; make)
	cp sparql-service/sparql sparql

BASE_CONTAINER=challenges-base

REPO=europe-west1-docker.pkg.dev/pivot-labs/pivot-labs
WEB_CONTAINER=${REPO}/web:${VERSION}
SPARQL_CONTAINER=${REPO}/sparql:${VERSION}

containers: all sparql-explorer sparql serve
	podman build -f Containerfile.base -t ${BASE_CONTAINER} \
	    --format docker
	podman build -f Containerfile.web -t ${WEB_CONTAINER} \
	    --format docker
	podman build -f Containerfile.sparql -t ${SPARQL_CONTAINER} \
	    --format docker

push:
	podman push --remove-signatures ${WEB_CONTAINER}
	podman push --remove-signatures ${SPARQL_CONTAINER}

run:
	podman run -d --name web \
		-p 8080/tcp --expose=8080 \
		${WEB_CONTAINER}
	podman run -d --name sparql -p 8089/tcp \
		${SPARQL_CONTAINER}

stop:
	podman rm -f web sparql

login:
	gcloud auth print-access-token | \
	    podman login -u oauth2accesstoken --password-stdin \
	        europe-west1-docker.pkg.dev

