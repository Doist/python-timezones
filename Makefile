VERSION := $(shell python timezones/__version__.py)

help:
	@echo "Usage: 'make clean' or 'make build' or 'make tag' or 'make upload'"


clean:
	rm -rf dist/*


build: clean
	python setup.py sdist bdist_wheel --universal


tag:
	git tag -l | grep -q v$(VERSION) || { \
		git tag v$(VERSION) && \
		git push && \
		git push --tags; \
	}


upload: tag build
	twine upload dist/*

.PHONY: help clean build tag upload
