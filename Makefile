BUILD_DIR := build
DIST_DIR := dist

default: clean test build

clean:
	$(RM) -r $(BUILD_DIR)/*
	$(RM) -r $(DIST_DIR)/*

build:
	python setup.py bdist_wheel

sdist:
	python setup.py sdist

test:
	coverage run -m pytest -vv && coverage html
