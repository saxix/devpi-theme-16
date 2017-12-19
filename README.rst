Custom theme for devpi-server
=============================

This is a custom theme for devpi-server

.. image:: https://raw.githubusercontent.com/saxix/devpi-theme-16/master/docs/home.png



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


open browser at `http://127.0.0.1:9000`.

Screenshots
-----------

index
~~~~~

.. image:: https://raw.githubusercontent.com/saxix/devpi-theme-16/master/docs/index.png
   :alt: Home

login
~~~~~

.. image:: https://raw.githubusercontent.com/saxix/devpi-theme-16/master/docs/login.png


remove package
~~~~~~~~~~~~~~

.. image:: https://raw.githubusercontent.com/saxix/devpi-theme-16/master/docs/remove.png

project version page
~~~~~~~~~~~~~~~~~~~~

.. image:: https://raw.githubusercontent.com/saxix/devpi-theme-16/master/docs/project.png


status page
~~~~~~~~~~~

.. image:: https://raw.githubusercontent.com/saxix/devpi-theme-16/master/docs/status.png


info page
~~~~~~~~~

.. image:: https://raw.githubusercontent.com/saxix/devpi-theme-16/master/docs/info.png


Links
-----

+--------------------+----------------+--------------+--------------------+
| Stable             | |master-build| | |master-cov| |                    |
+--------------------+----------------+--------------+--------------------+
| Development        | |dev-build|    | |dev-cov|    |                    |
+--------------------+----------------+--------------+--------------------+
| Project home page: |https://github.com/saxix/devpi-theme-16             |
+--------------------+----------------+-----------------------------------+
| Issue tracker:     |https://github.com/saxix/devpi-theme-16/issues?sort |
+--------------------+----------------+-----------------------------------+
| Download:          |http://pypi.python.org/pypi/devpi-theme-16/         |
+--------------------+----------------+-----------------------------------+


.. |master-build| image:: https://secure.travis-ci.org/saxix/devpi-theme-16.png?branch=master
                    :target: http://travis-ci.org/saxix/devpi-theme-16/

.. |master-cov| image:: https://codecov.io/gh/saxix/devpi-theme-16/branch/master/graph/badge.svg
                    :target: https://codecov.io/gh/saxix/devpi-theme-16

.. |dev-build| image:: https://secure.travis-ci.org/saxix/devpi-theme-16.png?branch=develop
                  :target: http://travis-ci.org/saxix/devpi-theme-16/

.. |dev-cov| image:: https://codecov.io/gh/saxix/devpi-theme-16/branch/develop/graph/badge.svg
                    :target: https://codecov.io/gh/saxix/devpi-theme-16

