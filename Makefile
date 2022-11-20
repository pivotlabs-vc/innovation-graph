
VERSION=1.0

PROJECT=challenges

all: sparql-explorer sparql
	rapper -i turtle -o ntriples ${PROJECT}.ttl > ${PROJECT}.ntriples
	rapper -i turtle -o rdfxml ${PROJECT}.ttl > ${PROJECT}.rdf
	rapper -i turtle -o json ${PROJECT}.ttl > ${PROJECT}.json
	rdfproc -n -s sqlite ${PROJECT}.db parse ${PROJECT}.ttl turtle

serve:
	go build proxy/serve.go

sparql-explorer:
	-rm -rf sparql-explorer
	git clone git@github.com:cybermaggedon/sparql-explorer
	(cd sparql-explorer &&npm install && ng build)

sparql:
	-rm -rf sparql-service
	git clone http://github.com/cybermaggedon/sparql-service
	(cd sparql-service; make)
	cp sparql-service/sparql sparql

BASE_CONTAINER=challenges-base
WEB_CONTAINER=docker.io/cybermaggedon/challenges-web
SPARQL_CONTAINER=docker.io/cybermaggedon/challenges-sparql

containers: sparql-explorer sparql serve build-base build-web build-sparql
	sudo ./build-base ${BASE_CONTAINER}
	sudo ./build-web ${BASE_CONTAINER} ${WEB_CONTAINER}:${VERSION}
	sudo ./build-sparql ${BASE_CONTAINER} ${SPARQL_CONTAINER}:${VERSION}
	sudo buildah tag ${WEB_CONTAINER}:${VERSION} ${WEB_CONTAINER}:latest
	sudo buildah tag ${SPARQL_CONTAINER}:${VERSION} \
		${SPARQL_CONTAINER}:latest

push:
	sudo buildah push ${WEB_CONTAINER}:${VERSION}
	sudo buildah push ${WEB_CONTAINER}:latest
	sudo buildah push ${SPARQL_CONTAINER}:${VERSION}
	sudo buildah push ${SPARQL_CONTAINER}:latest

run:
	sudo podman run -d --name web \
		-p 8080/tcp --expose=8080 \
		--ip=10.88.1.1 --add-host sparql:10.88.1.2 \
		${WEB_CONTAINER}:${VERSION}
	sudo podman run -d --name sparql -p 8089/tcp --ip=10.88.1.2 \
		${SPARQL_CONTAINER}:${VERSION}

stop:
	sudo podman rm -f web sparql

