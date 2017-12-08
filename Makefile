clean:
	rm -fr dist .tox

build:
	python setup.py sdist

test:
	tox
