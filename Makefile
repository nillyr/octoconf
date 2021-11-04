BUILD_DIR := build
DIST_DIR := dist

default: clean test build

clean:
	$(RM) -r $(BUILD_DIR)
	$(RM) -r $(DIST_DIR)

build:
	python setup.py bdist_wheel

sdist:
	python setup.py sdist

test:
	pytest -v

coverage:
	coverage run -m pytest -v -W ignore::UserWarning
	coverage html
