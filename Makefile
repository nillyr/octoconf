BUILD_DIR := build
DIST_DIR := dist

default: clean test wheel sdist epub pdf

clean:
	$(RM) -r $(BUILD_DIR)/*
	$(RM) -r $(DIST_DIR)/*

wheel:
	python setup.py bdist_wheel

sdist:
	python setup.py sdist

test:
	pytest -v

coverage:
	coverage run -m pytest -v -W error::UserWarning
	coverage html

epub:
	pandoc -o $(DIST_DIR)/octoreconf.epub docs/title.txt \
	docs/0x1-Introduction/0x1-Table_of_contents.md \
	docs/0x1-Introduction/0x2-License.md \
	docs/0x1-Introduction/0x3-Introduction.md \
	docs/0x2-User_Documentation/0x1-User_Documentation.md \
	docs/0x3-Developer_Documentation/0x1-Developer_Documentation.md

pdf:
	pandoc -o $(DIST_DIR)/octoreconf.pdf docs/title.txt \
	docs/0x1-Introduction/0x1-Table_of_contents.md \
	docs/0x1-Introduction/0x2-License.md \
	docs/0x1-Introduction/0x3-Introduction.md \
	docs/0x2-User_Documentation/0x1-User_Documentation.md \
	docs/0x3-Developer_Documentation/0x1-Developer_Documentation.md
