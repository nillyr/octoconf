BUILD_DIR := build
COV_DIR   := htmlcov
DIST_DIR  := dist
TEST_DIR  := tests/.ignore/pytest
TOX_DIR   := .tox

default: clean test build

clean:
	$(RM) -r $(BUILD_DIR)
	$(RM) -r $(COV_DIR)
	$(RM) -r $(DIST_DIR)
	$(RM) -r $(TEST_DIR)
	$(RM) -r $(TOX_DIR)
	find . -name "*.pyc" -exec rm -f {} +
	find . -name "*.pyo" -exec rm -f {} +
	find . -name "__pycache__" -exec rm -rf {} +
	find . -name ".pytest_cache" -exec rm -rf {} +

build:
	@test ! -d $(DIST_DIR) || $(RM) -r $(DIST_DIR)
	python -m build

test:
	tox -c tox.ini -e py3

coverage:
	coverage run -m pytest -v -W error::UserWarning
	coverage html
