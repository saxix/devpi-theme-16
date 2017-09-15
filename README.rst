Custom theme for devpi-server
=============================

This is a custom theme for devpi-server

Installation
------------

``devpi-theme-16`` needs to be installed alongside ``devpi-server``.

Simply install it with::

    pip install devpi-theme-16

For ``devpi-server`` there is no configuration needed to activate the plugin,
as it will automatically discover the plugin through calling hooks using the
setuptools entry points mechanism.


Contribute
----------

::

    $ source <VIRTUALENV>/bin/activate
    $ export THEME_16_ROOT=/tmp/theme-16
    $ pip install devpi-server devpi-web
    $ devpi-server init --serverdir $THEME_16_ROOT
    $ pip install -e .
    $ CHAMELEON_RELOAD=1 devpi-server --start --host 0.0.0.0 --port 9000 --serverdir $THEME_16_ROOT --threads=2 --debug ; tail -f $THEME_16_ROOT/.xproc/devpi-server/xprocess.log


open browser at http://127.0.0.1:9000.
