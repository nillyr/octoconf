BUILD_DIR := build
COV_DIR   := htmlcov
DIST_DIR  := dist
TEST_DIR  := octoconf_tests/.ignore/pytest

default: clean test wheel sdist

clean:
	$(RM) -r $(BUILD_DIR)
	$(RM) -r $(COV_DIR)
	$(RM) -r $(DIST_DIR)
	$(RM) -r $(TEST_DIR)
	find . -name "*.pyc" -exec rm -f {} +
	find . -name "*.pyo" -exec rm -f {} +
	find . -name "__pycache__" -exec rm -rf {} +
	find . -name ".pytest_cache" -exec rm -rf {} +

wheel:
	@test ! -d $(DIST_DIR) || $(RM) -r $(DIST_DIR)
	python setup.py bdist_wheel

sdist:
	python setup.py sdist

test:
	pytest -v

coverage:
	coverage run -m pytest -v -W error::UserWarning
	coverage html
