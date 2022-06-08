VERSION := $(shell poetry version --short)

help:
	@echo "Usage: 'make clean' or 'make build' or 'make tag' or 'make upload' or 'make test'"


clean:
	rm -rf dist/*


build: clean
	poetry build


tag:
	git tag -l | grep -q v$(VERSION) || { \
		git tag v$(VERSION) && \
		git push && \
		git push --tags; \
	}


upload: tag build
	poetry publish


GeoIP2-City-Test.mmdb:
	rm -f GeoIP2-City-Test.mmdb
	wget https://github.com/maxmind/MaxMind-DB/raw/main/test-data/GeoIP2-City-Test.mmdb


test: GeoIP2-City-Test.mmdb
	poetry run pytest


.PHONY: help clean build tag upload test
