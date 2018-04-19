CODECOV_TOKEN?=${CODECOV_TOKEN}

clean:
	rm -fr dist .tox

build:
	python setup.py sdist

test:
	tox -- codecov -e TOXENV -t ${CODECOV_TOKEN}

demo:
	mkdir -p ~build
	-devpi-server --theme src/ --port 8000 --debug --offline-mode --serverdir ~build --init
	-devpi-server --port 8000 --debug --serverdir ~build
