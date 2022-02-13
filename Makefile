BUILD_DIR := build
DIST_DIR := dist
COV_DIR := htmlcov
TEST_DIR := octoconf_tests/.ignore/pytest

default: clean test wheel sdist doc

clean:
	$(RM) -r $(BUILD_DIR)
	$(RM) -r $(DIST_DIR)
	$(RM) -r $(COV_DIR)
	$(RM) -r $(TEST_DIR)

wheel:
	python setup.py bdist_wheel

sdist:
	python setup.py sdist

test:
	pytest -v

coverage:
	coverage run -m pytest -v -W error::UserWarning
	coverage html

doc:
	pandoc -o $(DIST_DIR)/octoconf.pdf docs/title.txt \
	docs/0x1-Introduction/0x1-Table_of_contents.md \
	docs/0x1-Introduction/0x2-License.md \
	docs/0x1-Introduction/0x3-Introduction.md \
	docs/0x2-User_Documentation/0x1-User_Documentation.md
