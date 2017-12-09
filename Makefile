clean:
	rm -fr dist .tox

build:
	python setup.py sdist

test:
	tox

demo:
	mkdir -p ~build
#	devpi-server --theme src/ --port 8000 --debug --offline-mode --no-root-pypi --serverdir ~build --init
	.tox/py27/bin/devpi-server --port 8000 --debug --offline-mode --no-root-pypi --serverdir ~build
