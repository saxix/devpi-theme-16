#!/usr/bin/env python
import codecs
import os

import imp

import sys
from setuptools import setup, find_packages

ROOT = os.path.realpath(os.path.join(os.path.dirname(__file__)))
init = os.path.join(ROOT, 'src', 'devpi_theme_16', '__init__.py')

app = imp.load_source('devpi_theme', init)

reqs = 'install.py%d.pip' % sys.version_info[0]


def read(*files):
    content = ''
    for f in files:
        content += codecs.open(os.path.join(ROOT, f), 'r').read()
    return content


setup(name=app.NAME,
      version=app.__version__,
      description="Theme plugin for devpi server",
      url="",
      long_description=read('README.md'),
      maintainer="",
      maintainer_email="",
      license="MIT",
      extras_require={'test': ['pytest', 'pytest-pep8', 'pytest-cov',
                               'pytest-flakes', 'tox', 'webtest',
                               'devpi-server']},
      entry_points={
          'devpi_server': [
              "devpi-theme-16 = devpi_theme_16.main"]},
      install_requires=[
          'devpi-web'],
      include_package_data=True,
      package_dir={'': 'src'},
      packages=find_packages('src'),
      zip_safe=False
      )
