import logging

from test_devpi_server.conftest import gentmp, httpget, makemapp  # noqa
from test_devpi_server.conftest import maketestapp, makexom, mapp  # noqa
from test_devpi_server.conftest import pypiurls, testapp, pypistage  # noqa
# from test_devpi_server.conftest import dummyrequest, pypiurls, testapp  # noqa
from test_devpi_server.conftest import storage_info  # noqa
# from test_devpi_server.conftest import mock, pyramidconfig  # noqa
import pytest

(makexom,)  # shut up pyflakes


def pytest_configure():
    logging.getLogger().handlers = []
    logging.getLogger("").handlers = []
    logging.getLogger("devpi_server").handlers = []

    logging.getLogger().setLevel(logging.ERROR)
    logging.getLogger("devpi_server").setLevel(logging.ERROR)
    logging.getLogger("devpi_web").setLevel(logging.ERROR)


def pytest_addoption(parser):
    parser.addoption("--fast", help="skip functional/slow tests",
                     default=False,
                     action="store_true")


@pytest.fixture
def xom(request, makexom):
    import devpi_theme_16.main
    import devpi_web.main
    from devpi_theme_16.main import devpiserver_cmdline_run
    xom = makexom(plugins=[(devpi_web.main, None),
                           (devpi_theme_16.main, None)])
    from devpi_server.main import set_default_indexes
    with xom.keyfs.transaction(write=True):
        set_default_indexes(xom.model)
    devpiserver_cmdline_run(xom)
    return xom

#
# @pytest.yield_fixture
# def pyramidconfig2():
#     from pyramid.testing import setUp, tearDown
#     # from devpi_theme_16.main import includeme as i1
#     from devpi_lockdown.main import includeme as i2
#     config = setUp()
#     i2(config)
#     # i1(config)
#     yield config
#     tearDown()
#
#
# @pytest.yield_fixture
# def dummyrequest2(pyramidconfig2):
#     from pyramid.testing import DummyRequest
#     request = DummyRequest()
#     pyramidconfig2.begin(request=request)
#     yield request
#
#
# @pytest.fixture
# def testapp2(dummyrequest2, maketestapp, xom):
#     return maketestapp(xom)
